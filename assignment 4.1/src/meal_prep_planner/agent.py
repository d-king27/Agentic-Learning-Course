from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


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


@dataclass
class MealPreferences:
    meal_type: str
    dietary_preferences: str
    servings: int
    cooking_time_minutes: int | None = None
    allergies: str = "None"
    extra_preferences: str = "None"

    def to_prompt_text(self) -> str:
        cooking_time = (
            f"{self.cooking_time_minutes} minutes"
            if self.cooking_time_minutes
            else "Flexible"
        )

        return (
            f"Meal type: {self.meal_type}\n"
            f"Dietary preferences or restrictions: {self.dietary_preferences}\n"
            f"Servings: {self.servings}\n"
            f"Available cooking time: {cooking_time}\n"
            f"Allergies or ingredients to avoid: {self.allergies}\n"
            f"Extra preferences: {self.extra_preferences}"
        )


meal_plan_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a practical meal preparation assistant. Create clear, "
            "safe, and realistic meal plans that match the user's preferences, "
            "serving size, available time, and allergies.",
        ),
        (
            "human",
            """
Meal preparation details:

{meal_preferences}

Generate a detailed meal preparation plan with these sections:
1. Meal overview
2. Shopping list with quantities
3. Ingredient alternatives for allergies or preferences
4. Step-by-step cooking instructions
5. Timing plan
6. Serving tips
7. Side dish or beverage recommendations

Keep the instructions easy to follow and suitable for a home cook.
""".strip(),
        ),
    ]
)


class MealPrepPlannerAgent:
    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0.7,
        request_timeout: float = 45,
        max_retries: int = 1,
    ) -> None:
        load_local_env()
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4")
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            request_timeout=request_timeout,
            max_retries=max_retries,
        )

    def generate_plan(self, meal_preferences: MealPreferences) -> str:
        prompt = meal_plan_prompt_template.format_prompt(
            meal_preferences=meal_preferences.to_prompt_text(),
        ).to_messages()
        response = self.llm.invoke(prompt)
        return response.content.strip()

