# Assignment 2.1: Reflective Customer Feedback Agent

Objective: build an AI agent that critiques and refines its analysis of customer
feedback iteratively.

This assignment uses the Reflection Pattern for a text-analysis task. The agent
analyzes customer feedback, identifies sentiment, suggests business improvements,
then refines its own analysis over multiple iterations.

## Step 1: Set Up the Environment

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required libraries:

```powershell
pip install -r requirements.txt
pip install -e .
```

This installs LangChain, the OpenAI client, and the `langchain-openai`
integration package used by the current `ChatOpenAI` import.

Create a shared `.env` file at the course root:

```text
Agentic-Learning-Course/.env
```

Add your API key:

```text
OPEN_AI_KEY="your-api-key-here"
```

You can also choose a model in the same file:

```text
OPENAI_MODEL="gpt-4"
```

## Step 2: Define the Problem

The agent starts with this customer feedback:

```text
The delivery was late, and the packaging was damaged. However, the customer
service team was very helpful in resolving the issue.
```

## Step 3: Design the Reflective Agent

The agent should:

- Analyze sentiment: identify positive, negative, and neutral feedback.
- Suggest improvements: propose practical action items for the business.
- Refine insights: improve clarity, depth, and feasibility over iterations.

### Pseudocode

```text
START

DEFINE customer_feedback
DEFINE number_of_iterations

CREATE reflective_feedback_agent

FOR each iteration:

    SEND current_feedback_or_analysis to the agent

    ASK agent to analyze sentiment
        IDENTIFY positive feedback
        IDENTIFY negative feedback
        IDENTIFY neutral feedback
        SUMMARIZE the overall sentiment

    ASK agent to suggest action items
        ADDRESS late delivery
        ADDRESS damaged packaging
        PRESERVE strong customer service
        SUGGEST customer retention ideas

    ASK agent to refine the analysis
        MAKE suggestions clearer
        MAKE suggestions more actionable
        PRIORITIZE operational improvements
        REMOVE vague recommendations

    SAVE the analysis and refined analysis

    SET current_feedback_or_analysis to refined_analysis

END FOR

DISPLAY final refined analysis
DISPLAY all iteration outputs

END
```

## Step 4: Implement the Agent

The implementation uses LangChain chat prompts:

```text
1. Analysis prompt:
   - Categorizes sentiment.
   - Extracts positives and negatives.
   - Suggests business action items.

2. Revision prompt:
   - Refines the analysis.
   - Improves clarity and feasibility.
   - Produces stronger final recommendations.
```

The main implementation is in `src/feedback_reflection/agent.py`.

## Step 5: Test the Agent

Run:

```powershell
python -m feedback_reflection.main
```

For a quick smoke test, run one iteration first:

```powershell
python -m feedback_reflection.main --iterations 1
```

Observe how each iteration improves the analysis and recommendations.
The agent uses a 45-second request timeout so a slow API response does not appear
to hang forever.

## Expected Outcomes

Iteration 1 should identify mixed sentiment:

- Positive: helpful customer service.
- Negative: late delivery and damaged packaging.
- Suggested improvements: improve delivery timelines, improve packaging quality,
  and recognize effective customer service.

Later iterations should refine the suggestions into more operationally useful
actions, such as packaging quality control, route optimization, customer
retention incentives, and service-team reinforcement.

## Deliverables

- Python script for the reflective agent.
- Output log showing each iteration.
- Final refined analysis.
- Reflection report answering:
  - How did the suggestions evolve over iterations?
  - What parts of the Reflection Pattern were most effective?
  - How could this approach be applied to other text-analysis tasks?

## Project Structure

```text
assignment 2.1/
  pyproject.toml
  requirements.txt
  src/
    feedback_reflection/
      __init__.py
      agent.py
      main.py
```
