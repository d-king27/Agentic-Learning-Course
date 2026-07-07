from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


CUSTOMER_DATABASE: dict[str, dict[str, str]] = {
    "123": {
        "name": "Alice",
        "issue": "Payment not processed",
        "priority": "High",
        "account_status": "Active",
        "previous_contact": "Customer emailed yesterday asking for an update.",
        "channel": "Email",
        "sentiment": "Frustrated",
    },
    "456": {
        "name": "Bob",
        "issue": "Unable to log in",
        "priority": "Medium",
        "account_status": "Active",
        "previous_contact": "No previous contact recorded.",
        "channel": "Live chat",
        "sentiment": "Neutral",
    },
    "789": {
        "name": "Priya",
        "issue": "Order not delivered",
        "priority": "High",
        "account_status": "Active",
        "previous_contact": "Customer called twice in the last 48 hours.",
        "channel": "Phone",
        "sentiment": "Upset",
    },
    "321": {
        "name": "Marcus",
        "issue": "Wants to cancel subscription",
        "priority": "Low",
        "account_status": "Trial ending soon",
        "previous_contact": "Customer asked about pricing options last week.",
        "channel": "Email",
        "sentiment": "Calm",
    },
}


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
class CustomerRecord:
    customer_id: str
    name: str
    issue: str
    priority: str
    account_status: str
    previous_contact: str
    channel: str
    sentiment: str

    def to_prompt_text(self) -> str:
        return (
            f"Customer ID: {self.customer_id}\n"
            f"Name: {self.name}\n"
            f"Issue: {self.issue}\n"
            f"Priority: {self.priority}\n"
            f"Account status: {self.account_status}\n"
            f"Previous contact: {self.previous_contact}\n"
            f"Preferred channel: {self.channel}\n"
            f"Customer sentiment: {self.sentiment}"
        )


@dataclass
class SupportWorkflowResult:
    customer_record: CustomerRecord | None
    initial_plan: str
    refined_plan: str
    error: str | None = None


planning_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI support planner. Create efficient, empathetic, "
            "step-by-step resolution plans for customer support teams.",
        ),
        (
            "human",
            """
Customer details:

{customer_data}

Create an initial resolution plan with these sections:
1. Issue summary
2. Priority assessment
3. Step-by-step resolution plan
4. Customer communication plan
5. Escalation recommendation
6. Follow-up timeline

Make the plan practical for a support agent to execute.
""".strip(),
        ),
    ]
)


reflection_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI support quality reviewer. Improve resolution plans "
            "for clarity, efficiency, empathy, and operational usefulness.",
        ),
        (
            "human",
            """
Customer details:

{customer_data}

Initial resolution plan:

{initial_plan}

Refine the plan by:
- making the steps clearer and more specific
- matching the urgency to the priority level
- improving customer empathy
- adding fallback or escalation guidance where needed
- making the final output ready for a support agent to use

Return the refined plan only.
""".strip(),
        ),
    ]
)


class ToolUseAgent:
    def fetch_customer_data(self, customer_id: str) -> CustomerRecord | dict[str, str]:
        print(f"Tool Use Agent: fetching customer data for {customer_id}...")
        data = CUSTOMER_DATABASE.get(customer_id)

        if not data:
            return {"error": "Customer not found."}

        return CustomerRecord(customer_id=customer_id, **data)


class PlanningAgent:
    def __init__(self, llm: ChatOpenAI) -> None:
        self.llm = llm

    def create_resolution_plan(self, customer_record: CustomerRecord) -> str:
        print("Planning Agent: creating initial resolution plan...")
        prompt = planning_prompt_template.format_prompt(
            customer_data=customer_record.to_prompt_text(),
        ).to_messages()
        response = self.llm.invoke(prompt)
        return response.content.strip()


class ReflectionAgent:
    def __init__(self, llm: ChatOpenAI) -> None:
        self.llm = llm

    def refine_resolution_plan(
        self,
        customer_record: CustomerRecord,
        initial_plan: str,
    ) -> str:
        print("Reflection Agent: reviewing and refining plan...")
        prompt = reflection_prompt_template.format_prompt(
            customer_data=customer_record.to_prompt_text(),
            initial_plan=initial_plan,
        ).to_messages()
        response = self.llm.invoke(prompt)
        return response.content.strip()


class CustomerSupportOrchestrator:
    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0.7,
        request_timeout: float = 45,
        max_retries: int = 1,
    ) -> None:
        load_local_env()
        selected_model = model or os.getenv("OPENAI_MODEL", "gpt-4")
        llm = ChatOpenAI(
            model=selected_model,
            temperature=temperature,
            request_timeout=request_timeout,
            max_retries=max_retries,
        )
        self.tool_use_agent = ToolUseAgent()
        self.planning_agent = PlanningAgent(llm)
        self.reflection_agent = ReflectionAgent(llm)

    def run(self, customer_id: str) -> SupportWorkflowResult:
        normalized_customer_id = customer_id.strip()

        if not normalized_customer_id:
            return SupportWorkflowResult(
                customer_record=None,
                initial_plan="",
                refined_plan="",
                error="Customer ID cannot be empty.",
            )

        print(f"Starting unified support workflow for customer ID: {customer_id}...\n")
        customer_data = self.tool_use_agent.fetch_customer_data(normalized_customer_id)

        if isinstance(customer_data, dict) and "error" in customer_data:
            error = customer_data["error"]
            print(f"Fallback: {error}")
            return SupportWorkflowResult(
                customer_record=None,
                initial_plan="",
                refined_plan="",
                error=error,
            )

        if not isinstance(customer_data, CustomerRecord):
            return SupportWorkflowResult(
                customer_record=None,
                initial_plan="",
                refined_plan="",
                error="Unexpected customer data format.",
            )

        try:
            initial_plan = self.planning_agent.create_resolution_plan(customer_data)
            refined_plan = self.reflection_agent.refine_resolution_plan(
                customer_data,
                initial_plan,
            )
        except Exception as error:
            return SupportWorkflowResult(
                customer_record=customer_data,
                initial_plan="",
                refined_plan="",
                error=f"LLM workflow failed: {error}",
            )

        return SupportWorkflowResult(
            customer_record=customer_data,
            initial_plan=initial_plan,
            refined_plan=refined_plan,
        )

