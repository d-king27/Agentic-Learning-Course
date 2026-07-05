from __future__ import annotations

import json
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
class EventDetails:
    event_type: str
    date: str
    audience: str
    goals: str

    def to_prompt_text(self) -> str:
        return (
            f"Type: {self.event_type}\n"
            f"Date: {self.date}\n"
            f"Audience: {self.audience}\n"
            f"Goals: {self.goals}"
        )


planning_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI event planner. Create a detailed step-by-step plan "
            "for organizing a virtual event. Break the plan into practical "
            "phases and actionable tasks.",
        ),
        (
            "human",
            """
Event details:

{event_details}

Generate the event plan with:
1. Event summary
2. Phase-by-phase plan
3. Actionable checklist
4. Suggested timeline
5. Risks and mitigation steps
6. Success metrics

Keep the plan clear, practical, and easy to execute.
""".strip(),
        ),
    ]
)


checklist_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You convert event plans into concise JSON checklists. Return only valid JSON.",
        ),
        (
            "human",
            """
Convert this event plan into a JSON checklist.

Use this exact shape:
{{
  "tasks": [
    {{"phase": "Preparation", "task": "Define event topic and goals"}},
    {{"phase": "Promotion", "task": "Send invitations"}}
  ]
}}

Event plan:
{event_plan}
""".strip(),
        ),
    ]
)


class VirtualEventPlannerAgent:
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

    def generate_plan(self, event_details: EventDetails) -> str:
        prompt = planning_prompt_template.format_prompt(
            event_details=event_details.to_prompt_text(),
        ).to_messages()
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def generate_checklist(self, event_plan: str) -> list[dict[str, str]]:
        prompt = checklist_prompt_template.format_prompt(event_plan=event_plan).to_messages()
        response = self.llm.invoke(prompt)
        content = self._strip_code_fences(response.content.strip())

        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            return []

        tasks = payload.get("tasks", [])

        if not isinstance(tasks, list):
            return []

        checklist: list[dict[str, str]] = []

        for item in tasks:
            if not isinstance(item, dict):
                continue

            phase = str(item.get("phase", "")).strip()
            task = str(item.get("task", "")).strip()

            if phase and task:
                checklist.append({"phase": phase, "task": task})

        return checklist

    def run(self, event_details: EventDetails) -> tuple[str, list[dict[str, str]]]:
        event_plan = self.generate_plan(event_details)
        checklist = self.generate_checklist(event_plan)
        return event_plan, checklist

    def _strip_code_fences(self, text: str) -> str:
        if text.startswith("```json"):
            return text.split("```json", 1)[1].split("```", 1)[0].strip()

        if text.startswith("```"):
            return text.split("```", 1)[1].split("```", 1)[0].strip()

        return text

