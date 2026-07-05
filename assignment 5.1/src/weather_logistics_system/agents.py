from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


FORECAST_API_URL = "https://api.openweathermap.org/data/2.5/forecast"


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


def get_weather_api_key() -> str:
    api_key = os.getenv("OPEN_WEATHER_API_KEY") or os.getenv("OPENWEATHER_API_KEY")

    if api_key:
        return api_key

    raise RuntimeError(
        "Missing weather API key. Add OPEN_WEATHER_API_KEY to your .env file."
    )


@dataclass
class ForecastPoint:
    timestamp: str
    temperature_c: float
    feels_like_c: float
    condition: str
    description: str
    humidity: int
    wind_speed_mps: float
    precipitation_mm: float


@dataclass
class WeatherSummary:
    location: str
    country: str
    forecast_points: list[ForecastPoint]

    def to_prompt_text(self) -> str:
        lines = [f"Location: {self.location}, {self.country}", "Forecast periods:"]

        for point in self.forecast_points:
            lines.append(
                "- "
                f"{point.timestamp}: {point.temperature_c:.1f} C, "
                f"feels like {point.feels_like_c:.1f} C, "
                f"{point.description}, humidity {point.humidity}%, "
                f"wind {point.wind_speed_mps:.1f} m/s, "
                f"precipitation {point.precipitation_mm:.1f} mm"
            )

        return "\n".join(lines)


insight_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a weather logistics advisor in a multi-agent system. "
            "Use the forecast summary to generate practical, actionable "
            "recommendations for logistics planning.",
        ),
        (
            "human",
            """
Forecast summary:

{forecast_summary}

Generated chart path:
{chart_path}

Provide concise logistics recommendations with these sections:
1. Weather overview
2. Delivery or transport risks
3. Packaging recommendations
4. Staffing or scheduling recommendations
5. Overall logistics advice

Keep the advice grounded in the supplied forecast data.
""".strip(),
        ),
    ]
)


class DataGatheringAgent:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def fetch_forecast(self, location: str) -> dict[str, Any]:
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric",
        }
        response = requests.get(FORECAST_API_URL, params=params, timeout=20)
        payload: dict[str, Any] = response.json()

        if response.status_code != 200:
            message = payload.get("message", "Unable to fetch weather data.")
            raise RuntimeError(f"OpenWeather error for {location}: {message}")

        if "list" not in payload:
            raise RuntimeError("The API response did not include forecast data.")

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

    def summarize(self, raw_data: dict[str, Any], periods: int = 5) -> WeatherSummary:
        city = raw_data["city"]
        forecast_points = [
            self._parse_forecast_point(entry) for entry in raw_data["list"][:periods]
        ]

        return WeatherSummary(
            location=city.get("name", "Unknown"),
            country=city.get("country", ""),
            forecast_points=forecast_points,
        )

    def generate_insights(self, summary: WeatherSummary, chart_path: Path) -> str:
        prompt = insight_prompt_template.format_prompt(
            forecast_summary=summary.to_prompt_text(),
            chart_path=str(chart_path),
        ).to_messages()
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def _parse_forecast_point(self, entry: dict[str, Any]) -> ForecastPoint:
        rain = entry.get("rain", {}).get("3h", 0)
        snow = entry.get("snow", {}).get("3h", 0)
        weather = entry["weather"][0]

        return ForecastPoint(
            timestamp=entry["dt_txt"],
            temperature_c=float(entry["main"]["temp"]),
            feels_like_c=float(entry["main"]["feels_like"]),
            condition=weather["main"],
            description=weather["description"],
            humidity=int(entry["main"]["humidity"]),
            wind_speed_mps=float(entry.get("wind", {}).get("speed", 0)),
            precipitation_mm=float(rain) + float(snow),
        )


class VisualizationAgent:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_temperature_chart(self, summary: WeatherSummary) -> Path:
        times = [point.timestamp for point in summary.forecast_points]
        temperatures = [point.temperature_c for point in summary.forecast_points]
        labels = [timestamp.replace(" ", "\n") for timestamp in times]
        location_slug = self._slugify(summary.location)
        chart_path = self.output_dir / f"temperature_trends_{location_slug}.png"

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(labels, temperatures, marker="o", linewidth=2)
        ax.set_title(f"Temperature Trends for {summary.location}")
        ax.set_xlabel("Forecast time")
        ax.set_ylabel("Temperature (C)")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(chart_path, dpi=150)
        plt.close(fig)

        return chart_path.resolve()

    def _slugify(self, value: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
        return slug or "location"


class WeatherLogisticsSystem:
    def __init__(self, output_dir: Path | None = None) -> None:
        load_local_env()
        api_key = get_weather_api_key()
        default_output_dir = Path(__file__).resolve().parents[2] / "outputs"
        self.data_gathering_agent = DataGatheringAgent(api_key)
        self.data_processing_agent = DataProcessingAgent()
        self.visualization_agent = VisualizationAgent(output_dir or default_output_dir)

    def run(self, location: str) -> tuple[WeatherSummary, Path, str]:
        normalized_location = location.strip()

        if not normalized_location:
            raise RuntimeError("Please enter a location.")

        print(f"Data Gathering Agent: gathering weather data for {normalized_location}...")
        raw_data = self.data_gathering_agent.fetch_forecast(normalized_location)

        print("Data Processing Agent: summarizing forecast data...")
        summary = self.data_processing_agent.summarize(raw_data)

        print("Visualization Agent: creating temperature trend chart...")
        chart_path = self.visualization_agent.create_temperature_chart(summary)
        print("Visualization Agent: chart saved to:")
        print(chart_path)

        print("Data Processing Agent: generating logistics insights...")
        insights = self.data_processing_agent.generate_insights(summary, chart_path)

        return summary, chart_path, insights

