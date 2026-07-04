# Assignment 2: Reflective Code Critic Agent

Practical exercise: build a reflective agent that critiques and revises a code
snippet iteratively for better logic, efficiency, and readability.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required libraries:

```powershell
pip install -r requirements.txt
```

This installs LangChain, the OpenAI client, and the `langchain-openai`
integration package used by the current `ChatOpenAI` import.

Set your OpenAI API key by creating a `.env` file in the course root, the
assignment folder, or `src/`:

```text
OPEN_AI_KEY="your-api-key-here"
```

The recommended shared location is:

```text
Agentic-Learning-Course/.env
```

The code will automatically load this when the agent starts.

## Run

```powershell
python -m reflective_agent.main
```

## Step 2: Define the Problem

The starter program sends this sample code snippet through a
critique-and-revision loop:

```python
def sum_numbers(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total
```

You can edit `src/reflective_agent/main.py` to change the snippet or the number
of reflection rounds.

## Step 3: Design the Reflective Agent

The reflective agent should analyze a code snippet, critique it, suggest
improvements, and refine those suggestions over multiple rounds.

Because this assignment is focused on code analysis, the "sentiment" step can be
adapted to classify the tone or severity of each item of feedback:

- Positive: something the code already does well.
- Neutral: an observation that is useful but not urgent.
- Negative: a problem that should be improved.

### Pseudocode

```text
START

DEFINE sample_code
DEFINE number_of_reflection_rounds

CREATE reflective_agent

FOR each round from 1 to number_of_reflection_rounds:

    SEND current_code to reflective_agent

    ASK agent to analyze the code
        IDENTIFY strengths in the code
        IDENTIFY weaknesses in the code
        IDENTIFY readability issues
        IDENTIFY efficiency issues
        IDENTIFY logic or correctness risks

    ASK agent to categorize each feedback item
        IF feedback describes a strength:
            LABEL as positive
        ELSE IF feedback describes a minor observation:
            LABEL as neutral
        ELSE IF feedback describes a problem:
            LABEL as negative

    ASK agent to suggest improvements
        FOR each negative or neutral feedback item:
            PROPOSE a specific action
            EXPLAIN why the action improves the code
            CHECK that the action is practical and easy to apply

    ASK agent to refine the suggestions
        MAKE the suggestions clearer
        ADD missing details where useful
        REMOVE vague or unrealistic ideas
        PRIORITIZE the most valuable changes

    ASK agent to revise the code
        APPLY the refined suggestions
        KEEP the code readable
        KEEP the code correct
        AVOID unnecessary complexity

    SAVE the critique, categories, suggestions, and revised code

    SET current_code to revised_code

END FOR

DISPLAY final improved code
DISPLAY reflection history

END
```

### Build Steps

```text
1. Store the starting code snippet.
2. Create a prompt that asks the model to review the code.
3. Ask the model to classify feedback as positive, negative, or neutral.
4. Ask the model to turn negative and neutral feedback into concrete improvements.
5. Ask the model to refine those improvements for clarity, depth, and feasibility.
6. Ask the model to rewrite the code using the refined improvements.
7. Repeat the process for a fixed number of reflection rounds.
8. Print or save each round so the improvement process is visible.
```

## Step 4: Implement the Agent

The Python implementation uses LangChain chat prompts to create a reflective
agent with two main stages:

```text
1. Analysis prompt:
   - Reviews the code.
   - Categorizes feedback as positive, neutral, or negative.
   - Suggests actionable improvements.
   - Prioritizes the most useful changes.

2. Revision prompt:
   - Refines the analysis.
   - Improves clarity, depth, and feasibility.
   - Produces a revised version of the code.
```

The main implementation is in `src/reflective_agent/agent.py`.

## Project Structure

```text
assignment 2/
  pyproject.toml
  requirements.txt
  src/
    reflective_agent/
      __init__.py
      agent.py
      main.py
```
