from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


STOCK_API_URL = "https://www.alphavantage.co/query"
TIME_SERIES_KEY = "Time Series (5min)"


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
class IntradayPoint:
    timestamp: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int


@dataclass
class StockSummary:
    symbol: str
    last_refreshed: str
    latest: IntradayPoint
    previous: IntradayPoint | None
    recent_points: list[IntradayPoint]

    def to_prompt_text(self) -> str:
        latest = self.latest
        daily_change = "Not available"

        if self.previous:
            price_change = latest.close_price - self.previous.close_price
            price_change_percent = (price_change / self.previous.close_price) * 100
            daily_change = f"{price_change:+.2f} ({price_change_percent:+.2f}%)"

        oldest = self.recent_points[-1]
        recent_change = latest.close_price - oldest.close_price
        recent_change_percent = (recent_change / oldest.close_price) * 100
        average_volume = round(
            sum(point.volume for point in self.recent_points) / len(self.recent_points)
        )

        return (
            f"Symbol: {self.symbol}\n"
            f"Last refreshed: {self.last_refreshed}\n"
            f"Latest close: ${latest.close_price:.2f}\n"
            f"Latest interval change: {daily_change}\n"
            f"Recent period change: {recent_change:+.2f} ({recent_change_percent:+.2f}%)\n"
            f"Latest volume: {latest.volume:,}\n"
            f"Average recent volume: {average_volume:,}\n"
            f"Recent points analyzed: {len(self.recent_points)}"
        )


insight_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI analyst in a multi-agent stock analysis system. "
            "Use the supplied data summary to produce actionable insights. "
            "This is an educational exercise, not personal financial advice.",
        ),
        (
            "human",
            """
Data summary:

{data_summary}

Text chart:

{chart}

Generate insights with these sections:
1. Current position
2. Short-term trend
3. Volume observation
4. Actionable insight
5. Risk or limitation

Keep the response concise and grounded in the supplied data.
""".strip(),
        ),
    ]
)


class DataGatheringAgent:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def fetch_intraday_data(self, symbol: str) -> dict[str, Any]:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": "5min",
            "apikey": self.api_key,
        }
        response = requests.get(STOCK_API_URL, params=params, timeout=20)
        payload: dict[str, Any] = response.json()

        if response.status_code != 200:
            raise RuntimeError("Unable to fetch data.")

        if "Error Message" in payload:
            raise RuntimeError(payload["Error Message"])

        if "Note" in payload:
            raise RuntimeError(payload["Note"])

        if "Information" in payload:
            raise RuntimeError(payload["Information"])

        if TIME_SERIES_KEY not in payload:
            raise RuntimeError("The API response did not include intraday stock data.")

        return payload


class DataProcessingAgent:
    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0.7,
        request_timeout: float = 45,
        max_retries: int = 1,
    ) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4")
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            request_timeout=request_timeout,
            max_retries=max_retries,
        )

    def summarize(self, raw_data: dict[str, Any]) -> StockSummary:
        meta_data = raw_data.get("Meta Data", {})
        symbol = meta_data.get("2. Symbol", "N/A")
        last_refreshed = meta_data.get("3. Last Refreshed", "N/A")
        time_series = raw_data[TIME_SERIES_KEY]
        timestamps = sorted(time_series.keys(), reverse=True)
        recent_timestamps = timestamps[:12]
        recent_points = [
            self._parse_intraday_point(timestamp, time_series[timestamp])
            for timestamp in recent_timestamps
        ]

        latest = recent_points[0]
        previous = recent_points[1] if len(recent_points) > 1 else None

        return StockSummary(
            symbol=symbol,
            last_refreshed=last_refreshed,
            latest=latest,
            previous=previous,
            recent_points=recent_points,
        )

    def generate_insights(self, summary: StockSummary, chart: str) -> str:
        prompt = insight_prompt_template.format_prompt(
            data_summary=summary.to_prompt_text(),
            chart=chart,
        ).to_messages()
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def _parse_intraday_point(
        self,
        timestamp: str,
        values: dict[str, str],
    ) -> IntradayPoint:
        return IntradayPoint(
            timestamp=timestamp,
            open_price=float(values["1. open"]),
            high_price=float(values["2. high"]),
            low_price=float(values["3. low"]),
            close_price=float(values["4. close"]),
            volume=int(values["5. volume"]),
        )


class VisualizationAgent:
    def create_price_chart(self, points: list[IntradayPoint]) -> str:
        chronological_points = list(reversed(points))
        prices = [point.close_price for point in chronological_points]
        min_price = min(prices)
        max_price = max(prices)
        price_range = max(max_price - min_price, 0.01)
        lines = []

        for point in chronological_points:
            relative_position = (point.close_price - min_price) / price_range
            bar_length = max(1, round(relative_position * 30))
            time = point.timestamp.split(" ")[-1]
            lines.append(f"{time} ${point.close_price:>8.2f} | {'#' * bar_length}")

        return "\n".join(lines)


class MultiAgentStockSystem:
    def __init__(self) -> None:
        load_local_env()
        api_key = get_stock_api_key()
        self.data_gathering_agent = DataGatheringAgent(api_key)
        self.data_processing_agent = DataProcessingAgent()
        self.visualization_agent = VisualizationAgent()

    def run(self, symbol: str) -> tuple[StockSummary, str, str]:
        normalized_symbol = symbol.strip().upper()

        if not normalized_symbol:
            raise RuntimeError("Please enter a stock symbol.")

        print(f"Data Gathering Agent: gathering data for {normalized_symbol}...")
        raw_data = self.data_gathering_agent.fetch_intraday_data(normalized_symbol)

        print("Data Processing Agent: summarizing data...")
        summary = self.data_processing_agent.summarize(raw_data)

        print("Visualization Agent: creating text chart...")
        chart = self.visualization_agent.create_price_chart(summary.recent_points)

        print("Data Processing Agent: generating insights...")
        insights = self.data_processing_agent.generate_insights(summary, chart)

        return summary, chart, insights

