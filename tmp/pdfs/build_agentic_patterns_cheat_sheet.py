from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path("C:/Users/Dan/Documents/Codex/Agentic-Learning-Course")
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_PATH = OUTPUT_DIR / "agentic_design_patterns_cheat_sheet.pdf"


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#16324F"),
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#3E5267"),
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "Heading1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#16324F"),
            spaceBefore=12,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#24527A"),
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.3,
            leading=12.5,
            textColor=colors.HexColor("#1F2933"),
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#334E68"),
        ),
        "callout": ParagraphStyle(
            "Callout",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#102A43"),
            backColor=colors.HexColor("#EAF4FF"),
            borderColor=colors.HexColor("#9FB3C8"),
            borderWidth=0.6,
            borderPadding=7,
            spaceBefore=6,
            spaceAfter=8,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=6.7,
            leading=8.2,
            textColor=colors.HexColor("#102A43"),
            backColor=colors.HexColor("#F5F7FA"),
            borderColor=colors.HexColor("#CBD5E1"),
            borderWidth=0.5,
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=8,
        ),
    }


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def bullets(items: list[str], styles: dict[str, ParagraphStyle]) -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item, styles["body"]), leftIndent=10) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=14,
        bulletFontSize=6,
    )


def code_block(code: str, styles: dict[str, ParagraphStyle]) -> Preformatted:
    return Preformatted(code.strip(), styles["code"], maxLineLength=94)


def pattern_card(
    title: str,
    summary: str,
    use_when: list[str],
    benefits: list[str],
    pitfalls: list[str],
    code: str,
    styles: dict[str, ParagraphStyle],
) -> list:
    story: list = [
        p(title, styles["h1"]),
        p(summary, styles["body"]),
        p("Use When", styles["h2"]),
        bullets(use_when, styles),
        p("Benefits", styles["h2"]),
        bullets(benefits, styles),
        p("Watch For", styles["h2"]),
        bullets(pitfalls, styles),
        p("Boilerplate", styles["h2"]),
        code_block(code, styles),
    ]
    return story


def add_page_number(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#627D98"))
    canvas.drawRightString(A4[0] - 1.5 * cm, 1.0 * cm, f"Page {doc.page}")
    canvas.drawString(1.5 * cm, 1.0 * cm, "Agentic Design Patterns Cheat Sheet")
    canvas.restoreState()


def build_pdf() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        rightMargin=1.45 * cm,
        leftMargin=1.45 * cm,
        topMargin=1.35 * cm,
        bottomMargin=1.45 * cm,
    )
    story: list = []

    story.append(p("Agentic Design Patterns", styles["title"]))
    story.append(
        p(
            "Revision cheat sheet for the course assignments: reflection, tool use, "
            "planning, and multi-agent systems. Focus: what each pattern is for, "
            "why it helps, and reusable Python/LangChain boilerplates.",
            styles["subtitle"],
        )
    )
    story.append(
        p(
            "Core mental model: a useful agent is usually a loop around an LLM. "
            "It gathers context, applies a task-specific pattern, calls tools if "
            "needed, validates or refines the result, and returns an actionable output.",
            styles["callout"],
        )
    )

    overview_data = [
        [
            p("<b>Pattern</b>", styles["small"]),
            p("<b>Best For</b>", styles["small"]),
            p("<b>Main Benefit</b>", styles["small"]),
        ],
        [
            p("Reflection", styles["small"]),
            p("Critique, revision, quality improvement", styles["small"]),
            p("Improves first drafts through iterative self-review", styles["small"]),
        ],
        [
            p("Tool/API Use", styles["small"]),
            p("Live data, external systems, dynamic answers", styles["small"]),
            p("Grounds the model in real-world data", styles["small"]),
        ],
        [
            p("Planning", styles["small"]),
            p("Specific goals with constraints and steps", styles["small"]),
            p("Turns vague goals into executable workflows", styles["small"]),
        ],
        [
            p("Multi-Agent", styles["small"]),
            p("Complex workflows with separable responsibilities", styles["small"]),
            p("Improves modularity, clarity, and extensibility", styles["small"]),
        ],
    ]
    table = Table(overview_data, colWidths=[3.2 * cm, 6.5 * cm, 7.0 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#102A43")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#BCCCDC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend([table, Spacer(1, 10), PageBreak()])

    story.extend(
        pattern_card(
            "1. Reflection Pattern",
            "The agent generates an initial answer, critiques it, then revises it. "
            "This is useful when quality improves through feedback loops.",
            [
                "You need a better answer than the first model response.",
                "The task involves critique, code review, analysis, or refinement.",
                "You want visible improvement across iterations.",
            ],
            [
                "Encourages clearer, deeper, and more feasible outputs.",
                "Makes weaknesses explicit before revision.",
                "Good for deliverables that need an output log or reflection history.",
            ],
            [
                "Can become repetitive if the critique prompt is vague.",
                "Costs more tokens because each iteration calls the model again.",
                "Needs a stopping rule: fixed rounds, score threshold, or user approval.",
            ],
            """
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model=\"gpt-4\", temperature=0.7)

critique_prompt = ChatPromptTemplate.from_messages([
    (\"system\", \"Critique the draft and suggest practical fixes.\"),
    (\"human\", \"Draft:\\n{draft}\")
])

revise_prompt = ChatPromptTemplate.from_messages([
    (\"system\", \"Revise the draft using the critique.\"),
    (\"human\", \"Draft:\\n{draft}\\n\\nCritique:\\n{critique}\")
])

def reflective_agent(draft: str, rounds: int = 2) -> str:
    for _ in range(rounds):
        critique = llm.invoke(critique_prompt.format(draft=draft)).content
        draft = llm.invoke(revise_prompt.format(
            draft=draft, critique=critique
        )).content
    return draft
""",
            styles,
        )
    )

    story.append(PageBreak())
    story.extend(
        pattern_card(
            "2. Tool/API Use Pattern",
            "The agent calls an external tool first, then uses the model to interpret "
            "the result. This prevents the model from guessing current facts.",
            [
                "The answer depends on live or external data.",
                "You need weather, stocks, files, databases, APIs, or calculations.",
                "The model should explain data rather than invent it.",
            ],
            [
                "Grounds outputs in real data.",
                "Separates retrieval from interpretation.",
                "Makes failures easier to report when the API returns an error.",
            ],
            [
                "API keys must be loaded safely from environment variables.",
                "Raw JSON should be summarized before sending to the model.",
                "Handle timeouts, missing fields, and rate limits.",
            ],
            """
import os, requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model=os.getenv(\"OPENAI_MODEL\", \"gpt-4\"))
prompt = ChatPromptTemplate.from_messages([
    (\"system\", \"Explain the API data and recommend actions.\"),
    (\"human\", \"Data summary:\\n{summary}\")
])

def fetch_data(location: str) -> dict:
    r = requests.get(\"https://api.example.com/data\", params={
        \"q\": location, \"apikey\": os.getenv(\"API_KEY\")
    }, timeout=20)
    r.raise_for_status()
    return r.json()

def tool_using_agent(location: str) -> str:
    raw = fetch_data(location)
    summary = f\"temp={raw['main']['temp']}; condition={raw['weather'][0]['description']}\"
    return llm.invoke(prompt.format(summary=summary)).content
""",
            styles,
        )
    )

    story.append(PageBreak())
    story.extend(
        pattern_card(
            "3. Planning Pattern",
            "The agent collects a clear objective and structured parameters, then "
            "decomposes the goal into phases, steps, checklists, or instructions.",
            [
                "The task has a specific goal and constraints.",
                "The user needs an executable plan, not just an explanation.",
                "The output should include steps, timelines, lists, risks, or success criteria.",
            ],
            [
                "Reduces vague responses by giving the model boundaries.",
                "Turns broad goals into actionable tasks.",
                "Works well for most specific-purpose agents, not just event or meal planning.",
            ],
            [
                "Too much structure can make casual chat feel rigid.",
                "Missing constraints can cause impractical plans.",
                "Complex plans may need progress tracking or revision.",
            ],
            """
from dataclasses import dataclass
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

@dataclass
class PlanRequest:
    objective: str
    constraints: str
    preferences: str
    output_format: str

prompt = ChatPromptTemplate.from_messages([
    (\"system\", \"Break the objective into actionable steps.\"),
    (\"human\", \"Objective: {objective}\\nConstraints: {constraints}\\n\"
              \"Preferences: {preferences}\\nReturn: {output_format}\")
])

def planning_agent(request: PlanRequest) -> str:
    return ChatOpenAI(model=\"gpt-4\").invoke(
        prompt.format(**request.__dict__)
    ).content
""",
            styles,
        )
    )

    story.append(PageBreak())
    story.extend(
        pattern_card(
            "4. Multi-Agent Pattern",
            "The workflow is split between specialist agents. Each agent owns a "
            "specific responsibility, and an orchestrator coordinates the handoff.",
            [
                "The task naturally has separate stages.",
                "Different parts need different tools or prompts.",
                "You want easier debugging and extension.",
            ],
            [
                "Improves clarity through division of labor.",
                "Makes each part easier to test independently.",
                "Lets you add new agents, such as visualization or alerts, without rewriting everything.",
            ],
            [
                "Agent boundaries should be real, not artificial.",
                "Handoffs need clean data structures.",
                "The orchestrator should make the workflow order obvious.",
            ],
            """
class DataGatheringAgent:
    def run(self, query: str) -> dict:
        return fetch_external_data(query)

class DataProcessingAgent:
    def summarize(self, raw: dict) -> dict:
        return {\"metric\": raw[\"value\"], \"trend\": \"up\"}
    def generate_insights(self, summary: dict) -> str:
        return llm.invoke(insight_prompt.format(summary=summary)).content

class VisualizationAgent:
    def create_chart(self, summary: dict) -> str:
        return save_chart(summary, \"outputs/chart.png\")

class MultiAgentSystem:
    def run(self, query: str) -> tuple[str, str]:
        raw = DataGatheringAgent().run(query)
        summary = DataProcessingAgent().summarize(raw)
        chart = VisualizationAgent().create_chart(summary)
        insights = DataProcessingAgent().generate_insights(summary)
        return insights, chart
""",
            styles,
        )
    )

    story.append(p("5. Shared Environment Boilerplate", styles["h1"]))
    story.append(
        p(
            "Most assignments used a shared course-level .env file. This keeps keys "
            "out of source code and lets multiple projects reuse the same credentials.",
            styles["body"],
        )
    )
    story.append(
        code_block(
            """
import os
from pathlib import Path

def load_local_env() -> None:
    for env_path in [Path(__file__).resolve().parents[3] / \".env\"]:
        if not env_path.exists():
            continue
        for line in env_path.read_text(encoding=\"utf-8\").splitlines():
            if not line.strip() or \"=\" not in line:
                continue
            key, value = line.split(\"=\", 1)
            os.environ.setdefault(
                key.strip().strip('\"').strip(\"'\"),
                value.strip().strip('\"').strip(\"'\"),
            )
    os.environ.setdefault(\"OPENAI_API_KEY\", os.getenv(\"OPEN_AI_KEY\", \"\"))
""",
            styles,
        )
    )

    story.append(PageBreak())
    story.append(p("6. Design Decision Checklist", styles["h1"]))
    checklist = [
        "<b>Define the objective:</b> what is the agent trying to achieve?",
        "<b>Collect parameters:</b> what inputs, preferences, constraints, or keys matter?",
        "<b>Choose the pattern:</b> reflection, tool use, planning, multi-agent, or a combination.",
        "<b>Separate responsibilities:</b> API calls, summarization, reasoning, visualization, and output.",
        "<b>Use structured prompts:</b> specify role, context, expected sections, and constraints.",
        "<b>Summarize before prompting:</b> send compact useful data, not huge raw JSON.",
        "<b>Handle errors:</b> missing keys, API failure, rate limits, empty data, timeouts.",
        "<b>Make deliverables visible:</b> print logs, save outputs, show chart paths, keep screenshots.",
        "<b>Reflect on value:</b> explain why the pattern made the agent better than a simple chatbot.",
    ]
    story.append(bullets(checklist, styles))

    story.append(p("7. Common Assignment Phrasing", styles["h1"]))
    phrasing_rows = [
        [
            p("<b>Concept</b>", styles["small"]),
            p("<b>Useful wording for reflection reports</b>", styles["small"]),
        ],
        [
            p("Reflection", styles["small"]),
            p(
                "The agent improved its output by critiquing and revising earlier responses.",
                styles["small"],
            ),
        ],
        [
            p("Tool Use", styles["small"]),
            p(
                "The external API grounded the response in current, real-world data.",
                styles["small"],
            ),
        ],
        [
            p("Planning", styles["small"]),
            p(
                "Structured objectives and parameters helped the model decompose the task into actionable steps.",
                styles["small"],
            ),
        ],
        [
            p("Multi-Agent", styles["small"]),
            p(
                "Specialized agents improved clarity by separating data gathering, processing, and presentation.",
                styles["small"],
            ),
        ],
    ]
    phrasing_table = Table(phrasing_rows, colWidths=[3.5 * cm, 13.2 * cm])
    phrasing_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#BCCCDC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(phrasing_table)

    story.append(Spacer(1, 10))
    story.append(
        p(
            "Fast rule: open chat can stay flexible; specific-goal agents usually "
            "benefit from structured data, constraints, expected output shape, and "
            "a pattern that matches the workflow.",
            styles["callout"],
        )
    )

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT_PATH)
