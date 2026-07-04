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
        Path(__file__).resolve().parents[1] / ".env",
        Path(__file__).resolve().parents[2] / ".env",
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


SYSTEM_PROMPT = """
You are a reflective Python code analysis agent.
Your job is to critique and improve code through reflection.
Analyze logic, efficiency, readability, maintainability, and correctness.
Categorize feedback as positive, neutral, or negative.
Suggest practical improvements, then refine those insights before revising the code.
""".strip()


analysis_prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template(
            """
Analyze the Python code below.

Return your analysis with these sections:
1. Sentiment categories: positive, neutral, and negative feedback.
2. Improvement suggestions: actionable steps for negative or neutral feedback.
3. Revision priorities: the most important changes to make first.

Code:
```python
{code}
```
""".strip()
        ),
    ]
)


revision_prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template(
            """
Refine the following code analysis so it is clearer, deeper, and more feasible.
Then provide a revised version of the code.

Return your answer with these sections:
1. Refined analysis
2. Revised code

Original code:
```python
{code}
```

Analysis:
{analysis}
""".strip()
        ),
    ]
)


@dataclass
class ReflectionResult:
    round_number: int
    analysis: str
    refined_analysis: str
    revised_code: str

    @property
    def critique(self) -> str:
        return self.analysis


class ReflectiveCodeAgent:
    def __init__(self, model: str = "gpt-4", temperature: float = 0.7) -> None:
        load_local_env()
        self.llm = ChatOpenAI(model=model, temperature=temperature)

    def analyze(self, code: str) -> str:
        analysis_prompt = analysis_prompt_template.format_prompt(code=code).to_messages()
        analysis_response = self.llm.invoke(analysis_prompt)
        return analysis_response.content.strip()

    def refine_and_revise(self, code: str, analysis: str) -> tuple[str, str]:
        revision_prompt = revision_prompt_template.format_prompt(
            code=code,
            analysis=analysis,
        ).to_messages()
        revision_response = self.llm.invoke(revision_prompt)
        refined_output = revision_response.content.strip()
        revised_code = self._extract_revised_code(refined_output)
        return refined_output, revised_code

    def improve(self, code: str, rounds: int = 3) -> list[ReflectionResult]:
        current_code = code
        results: list[ReflectionResult] = []

        for round_number in range(1, rounds + 1):
            analysis = self.analyze(current_code)
            refined_analysis, revised_code = self.refine_and_revise(
                current_code,
                analysis,
            )
            results.append(
                ReflectionResult(
                    round_number=round_number,
                    analysis=analysis,
                    refined_analysis=refined_analysis,
                    revised_code=revised_code,
                )
            )
            current_code = revised_code

        return results

    def _extract_revised_code(self, refined_output: str) -> str:
        if "```python" in refined_output:
            return refined_output.split("```python", 1)[1].split("```", 1)[0].strip()

        if "```" in refined_output:
            return refined_output.split("```", 1)[1].split("```", 1)[0].strip()

        return refined_output
