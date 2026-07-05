from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


STOCK_API_URL = "https://www.alphavantage.co/query"


def load_local_env() -> None:
    env_paths = [
        Path(__file__).resolve().parents[3] / ".env",
        Path(__file__).resolve().parents[2] / ".env",
        Path(__file__).resolve().parents[1] / ".env",
    ]

    for env_path in env_paths:
        if not env_path.exists():
            continue

        for line in env_path.read_text(encoding="utf-8").splitlines():
            clean_line = line.strip()

            if not clean_line or clean_line.startswith("#") or "=" not in clean_line:
                continue

            key, value = clean_line.split("=", 1)
            key = key.strip().strip('"').strip("'")
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)

    if "OPEN_AI_KEY" in os.environ and "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = os.environ["OPEN_AI_KEY"]


def get_stock_api_key() -> str:
    api_key = os.getenv("STOCK_MARKET_API_KEY")

    if api_key:
        return api_key

    raise RuntimeError(
        "Missing stock market API key. Add STOCK_MARKET_API_KEY to your .env file."
    )


@dataclass
class DailyStockPoint:
    date: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int


@dataclass
class StockAnalysis:
    symbol: str
    latest: DailyStockPoint
    previous: DailyStockPoint | None
    five_day_change_percent: float | None
    average_volume: int
    volume_vs_average_percent: float

    def to_prompt_text(self) -> str:
        daily_change = "Not available"

        if self.previous:
            change = self.latest.close_price - self.previous.close_price
            change_percent = (change / self.previous.close_price) * 100
            daily_change = f"{change:+.2f} ({change_percent:+.2f}%)"

        five_day_change = (
            f"{self.five_day_change_percent:+.2f}%"
            if self.five_day_change_percent is not None
            else "Not available"
        )

        return (
            f"Symbol: {self.symbol}\n"
            f"Latest trading date: {self.latest.date}\n"
            f"Open: ${self.latest.open_price:.2f}\n"
            f"High: ${self.latest.high_price:.2f}\n"
            f"Low: ${self.latest.low_price:.2f}\n"
            f"Close: ${self.latest.close_price:.2f}\n"
            f"Volume: {self.latest.volume:,}\n"
            f"Daily close change: {daily_change}\n"
            f"Five-day close change: {five_day_change}\n"
            f"Average recent volume: {self.average_volume:,}\n"
            f"Latest volume vs average: {self.volume_vs_average_percent:+.2f}%"
        )


recommendation_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a stock market advisor for an educational coding exercise. "
            "Analyze the supplied market data and provide a buy, sell, or hold "
            "style recommendation with clear reasoning. Do not present the answer "
            "as personalized financial advice.",
        ),
        (
            "human",
            """
Here is the stock analysis:

{stock_analysis}

Generate a concise recommendation with these sections:
1. Performance summary
2. Trend and volume insight
3. Recommendation: buy, sell, or hold
4. Risk notes
5. What additional data would improve the decision
""".strip(),
        ),
    ]
)


class StockMarketAdvisorAgent:
    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0.7,
        request_timeout: float = 45,
        max_retries: int = 1,
    ) -> None:
        load_local_env()
        self.stock_api_key = get_stock_api_key()
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4")
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            request_timeout=request_timeout,
            max_retries=max_retries,
        )

    def fetch_stock_data(self, symbol: str) -> dict[str, Any]:
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.stock_api_key,
        }

        response = requests.get(STOCK_API_URL, params=params, timeout=20)
        payload: dict[str, Any] = response.json()

        if response.status_code != 200:
            raise RuntimeError("Unable to fetch stock data.")

        if "Error Message" in payload:
            raise RuntimeError(payload["Error Message"])

        if "Note" in payload:
            raise RuntimeError(payload["Note"])

        if "Information" in payload:
            raise RuntimeError(payload["Information"])

        if "Time Series (Daily)" not in payload:
            raise RuntimeError("The API response did not include daily stock data.")

        return payload

    def analyze_stock_data(self, symbol: str, stock_data: dict[str, Any]) -> StockAnalysis:
        daily_data = stock_data["Time Series (Daily)"]
        dates = sorted(daily_data.keys(), reverse=True)
        recent_dates = dates[:5]
        points = [self._parse_daily_point(date, daily_data[date]) for date in recent_dates]

        latest = points[0]
        previous = points[1] if len(points) > 1 else None
        oldest = points[-1]
        five_day_change_percent = None

        if len(points) > 1:
            five_day_change_percent = (
                (latest.close_price - oldest.close_price) / oldest.close_price
            ) * 100

        average_volume = round(sum(point.volume for point in points) / len(points))
        volume_vs_average_percent = (
            (latest.volume - average_volume) / average_volume
        ) * 100

        return StockAnalysis(
            symbol=symbol.upper(),
            latest=latest,
            previous=previous,
            five_day_change_percent=five_day_change_percent,
            average_volume=average_volume,
            volume_vs_average_percent=volume_vs_average_percent,
        )

    def generate_recommendation(self, stock_analysis: StockAnalysis) -> str:
        prompt = recommendation_prompt_template.format_prompt(
            stock_analysis=stock_analysis.to_prompt_text(),
        ).to_messages()
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def run(self, symbol: str) -> tuple[StockAnalysis, str]:
        normalized_symbol = symbol.strip().upper()

        if not normalized_symbol:
            raise RuntimeError("Please enter a stock symbol.")

        stock_data = self.fetch_stock_data(normalized_symbol)
        stock_analysis = self.analyze_stock_data(normalized_symbol, stock_data)
        recommendation = self.generate_recommendation(stock_analysis)
        return stock_analysis, recommendation

    def _parse_daily_point(self, date: str, values: dict[str, str]) -> DailyStockPoint:
        return DailyStockPoint(
            date=date,
            open_price=float(values["1. open"]),
            high_price=float(values["2. high"]),
            low_price=float(values["3. low"]),
            close_price=float(values["4. close"]),
            volume=int(values["5. volume"]),
        )
