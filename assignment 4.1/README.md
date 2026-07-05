# Assignment 4.1: Meal Preparation Planning Agent

Objective: build an interactive AI agent that creates meal preparation plans
from user preferences.

The agent collects meal type, dietary restrictions, servings, available cooking
time, allergies, and optional preferences. It then generates a meal plan with a
shopping list, step-by-step cooking instructions, serving tips, and optional side
dish or beverage suggestions.

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

Use the shared course-level `.env` file for your OpenAI key:

```text
Agentic-Learning-Course/.env
```

Example:

```text
OPEN_AI_KEY="your-openai-api-key-here"
OPENAI_MODEL="gpt-4"
```

## Step 2: Define the Planning Agent

The planning agent:

```text
1. Accepts meal preparation details from the user.
2. Formats those details into a structured prompt.
3. Asks the language model to act as a meal preparation assistant.
4. Generates a practical plan with:
   - shopping list
   - cooking instructions
   - timing notes
   - allergy-aware alternatives
   - side dish or beverage recommendations
```

## Step 3: Build User Interaction

Interactive mode:

```powershell
python -m meal_prep_planner.main
```

Single-run mode:

```powershell
python -m meal_prep_planner.main --meal-type "Dinner" --dietary "Vegetarian" --servings 2
```

With personalization:

```powershell
python -m meal_prep_planner.main --meal-type "Dinner" --dietary "Vegetarian" --servings 2 --time 30 --allergies "peanuts" --preferences "high protein"
```

## Expected Output

The generated meal plan should include:

- Shopping list of ingredients.
- Step-by-step cooking instructions.
- Timing and preparation notes.
- Optional tips for serving.
- Alternative ingredients where useful.
- Side dish or beverage recommendations.

## Deliverables

- Python script: submit the complete implementation.
- Demo evidence: include screenshots, terminal output, or a short demo video
  showing the agent in action.
- Brief write-up: explain how the agent works and any implementation challenges.
- Evaluation notes:
  - Completeness: does it collect the required meal details?
  - Clarity: are the shopping list and instructions easy to follow?
  - Interactivity: does the agent engage the user effectively?
  - Bonus: were personalization features implemented?

## Project Structure

```text
assignment 4.1/
  pyproject.toml
  requirements.txt
  src/
    meal_prep_planner/
      __init__.py
      agent.py
      main.py
```
