# Assignment 3: Weather Recommendation Agent

Objective: design and implement a weather recommendation agent that fetches
live weather data and generates tailored suggestions based on current
conditions.

The agent combines:

- OpenWeatherMap for real-time weather data.
- LangChain and OpenAI for tailored recommendations.
- Optional user preferences such as outdoor activities or travel safety tips.

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

## Step 2: Configure API Keys

Use the shared course-level `.env` file:

```text
Agentic-Learning-Course/.env
```

Add your keys:

```text
OPEN_AI_KEY="your-openai-api-key-here"
OPENWEATHER_API_KEY="your-openweather-api-key-here"
OPENAI_MODEL="gpt-4"
```

The code also accepts `OPENAI_API_KEY`, `WEATHER_API_KEY`,
`OPEN_WEATHER_API_KEY`, or `OPENWEATHERMAP_API_KEY` if you already used one of
those names.

## Step 3: Understand the Workflow

```text
1. Accept a city name from the user.
2. Fetch current weather data from OpenWeatherMap.
3. Extract useful weather details:
   - temperature
   - feels-like temperature
   - conditions
   - humidity
   - wind speed
4. Send the weather summary to the language model.
5. Generate tailored recommendations for clothing, travel, activities, and
   safety.
```

## Step 4: Run the Agent

Interactive mode:

```powershell
python -m weather_recommendation.main
```

Single-city mode:

```powershell
python -m weather_recommendation.main --city "London"
```

With an extra preference:

```powershell
python -m weather_recommendation.main --city "London" --preference "outdoor activities"
```

## Step 5: Test Your Agent

Run the agent for at least three cities and save the outputs for your sample
runs deliverable.

Example cities:

```text
London
New York
Tokyo
```

## Deliverables

- Python script: submit the complete code.
- Sample runs: include output for at least three different city inputs.
- Reflection report: explain how the agent fetches and processes weather data,
  and discuss the value of combining APIs with generative AI.
- Reflection questions:
  - How does the agent dynamically adjust its recommendations based on the
    weather data?
  - What challenges did you face in integrating the weather API and AI
    workflows?
  - How could this agent be extended to include hourly weather updates or
    multi-day forecasts?

## Project Structure

```text
assignment 3/
  pyproject.toml
  requirements.txt
  src/
    weather_recommendation/
      __init__.py
      agent.py
      main.py
```
