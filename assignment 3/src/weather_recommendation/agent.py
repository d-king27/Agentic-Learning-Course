from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"


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
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)

    if "OPEN_AI_KEY" in os.environ and "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = os.environ["OPEN_AI_KEY"]


def get_weather_api_key() -> str:
    key_names = [
        "OPENWEATHER_API_KEY",
        "OPENWEATHERMAP_API_KEY",
        "OPEN_WEATHER_API_KEY",
        "WEATHER_API_KEY",
    ]

    for key_name in key_names:
        api_key = os.getenv(key_name)
        if api_key:
            return api_key

    accepted_names = ", ".join(key_names)
    raise RuntimeError(
        "Missing OpenWeather API key. Add one of these to your .env file: "
        f"{accepted_names}."
    )


@dataclass
class WeatherReport:
    location: str
    temperature_c: float
    feels_like_c: float
    condition: str
    description: str
    humidity: int
    wind_speed_mps: float

    def to_prompt_text(self) -> str:
        return (
            f"Location: {self.location}\n"
            f"Temperature: {self.temperature_c} C\n"
            f"Feels like: {self.feels_like_c} C\n"
            f"Condition: {self.condition}\n"
            f"Description: {self.description}\n"
            f"Humidity: {self.humidity}%\n"
            f"Wind speed: {self.wind_speed_mps} m/s"
        )


recommendation_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant that provides practical, personalized "
            "recommendations based on live weather data.",
        ),
        (
            "human",
            """
Here is the weather data:

{weather_data}

User preference:
{preference}

Generate tailored recommendations with these sections:
1. Quick weather summary
2. What to wear
3. Travel or safety advice
4. Activity recommendations
5. Anything to carry

Keep the advice concise, specific, and useful.
""".strip(),
        ),
    ]
)


class WeatherRecommendationAgent:
    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0.7,
        request_timeout: float = 45,
        max_retries: int = 1,
    ) -> None:
        load_local_env()
        self.weather_api_key = get_weather_api_key()
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4")
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            request_timeout=request_timeout,
            max_retries=max_retries,
        )

    def fetch_weather_data(self, location: str) -> WeatherReport:
        params = {
            "q": location,
            "appid": self.weather_api_key,
            "units": "metric",
        }

        response = requests.get(WEATHER_API_URL, params=params, timeout=20)
        payload: dict[str, Any] = response.json()

        if response.status_code != 200:
            message = payload.get("message", "Unable to fetch weather data.")
            raise RuntimeError(f"OpenWeather error for {location}: {message}")

        weather = payload["weather"][0]
        main = payload["main"]
        wind = payload.get("wind", {})
        resolved_location = f"{payload.get('name', location)}, {payload.get('sys', {}).get('country', '')}".strip(", ")

        return WeatherReport(
            location=resolved_location,
            temperature_c=main["temp"],
            feels_like_c=main["feels_like"],
            condition=weather["main"],
            description=weather["description"],
            humidity=main["humidity"],
            wind_speed_mps=wind.get("speed", 0),
        )

    def generate_recommendations(
        self,
        weather_report: WeatherReport,
        preference: str = "general recommendations",
    ) -> str:
        prompt = recommendation_prompt_template.format_prompt(
            weather_data=weather_report.to_prompt_text(),
            preference=preference,
        ).to_messages()
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def run(
        self,
        location: str,
        preference: str = "general recommendations",
    ) -> tuple[WeatherReport, str]:
        weather_report = self.fetch_weather_data(location)
        recommendations = self.generate_recommendations(weather_report, preference)
        return weather_report, recommendations

