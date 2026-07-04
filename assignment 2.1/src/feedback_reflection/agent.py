from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
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
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)

    if "OPEN_AI_KEY" in os.environ and "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = os.environ["OPEN_AI_KEY"]


analysis_prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are a customer feedback analyst. Analyze the feedback below."
        ),
        HumanMessagePromptTemplate.from_template(
            """
Customer feedback:
{feedback}

Return your response with these sections:
1. Overall sentiment
2. Positive feedback
3. Negative feedback
4. Neutral feedback
5. Suggested business action items
""".strip()
        ),
    ]
)


revision_prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "Refine the following analysis to improve clarity and suggestions."
        ),
        HumanMessagePromptTemplate.from_template(
            """
Analysis to refine:
{analysis}

Improve the analysis by:
- making the sentiment summary clearer
- making the action items more specific and feasible
- prioritizing operational fixes and customer satisfaction
- preserving useful positive insights

Return the refined analysis only.
""".strip()
        ),
    ]
)


@dataclass
class FeedbackReflectionResult:
    iteration: int
    analysis: str
    refined_analysis: str


class ReflectiveFeedbackAgent:
    def __init__(self, model: str = "gpt-4", temperature: float = 0.7) -> None:
        load_local_env()
        self.llm = ChatOpenAI(model=model, temperature=temperature)

    def analyze(self, feedback: str) -> str:
        analysis_prompt = analysis_prompt_template.format_prompt(
            feedback=feedback,
        ).to_messages()
        analysis_response = self.llm.invoke(analysis_prompt)
        return analysis_response.content.strip()

    def refine(self, analysis: str) -> str:
        revision_prompt = revision_prompt_template.format_prompt(
            analysis=analysis,
        ).to_messages()
        revision_response = self.llm.invoke(revision_prompt)
        return revision_response.content.strip()

    def run(self, feedback: str, iterations: int = 3) -> list[FeedbackReflectionResult]:
        current_input = feedback
        results: list[FeedbackReflectionResult] = []

        for iteration in range(1, iterations + 1):
            analysis = self.analyze(current_input)
            refined_analysis = self.refine(analysis)
            results.append(
                FeedbackReflectionResult(
                    iteration=iteration,
                    analysis=analysis,
                    refined_analysis=refined_analysis,
                )
            )
            current_input = refined_analysis

        return results
