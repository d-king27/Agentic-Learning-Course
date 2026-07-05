# Assignment 5.1: Multi-Agent Weather Logistics System

Objective: design and implement a multi-agent system with three collaborating
agents:

- Data Gathering Agent: fetches forecast data from OpenWeatherMap.
- Data Processing Agent: analyzes the collected weather data and generates
  logistics insights.
- Visualization Agent: creates a temperature trend chart.

The graph is saved to the project `outputs/` folder, and the command line prints
the exact file path after generation.

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

Use the shared course-level `.env` file for your keys:

```text
Agentic-Learning-Course/.env
```

Example:

```text
OPEN_AI_KEY="your-openai-api-key-here"
OPENAI_MODEL="gpt-4"
OPEN_WEATHER_API_KEY="your-openweather-api-key-here"
```

The code also accepts `OPENWEATHER_API_KEY`, but `OPEN_WEATHER_API_KEY` is the
recommended name for this project.

## Step 2: Understand the Workflow

```text
1. User enters a location.
2. Data Gathering Agent fetches forecast data from OpenWeatherMap.
3. Data Processing Agent extracts the next forecast periods and summarizes:
   - temperature
   - weather conditions
   - wind speed
   - humidity
   - rain or snow risk
4. Data Processing Agent sends that summary to the language model.
5. Visualization Agent creates a PNG chart of temperature trends.
6. The system prints logistics insights and the saved chart path.
```

## Step 3: Run the System

Interactive mode:

```powershell
python -m weather_logistics_system.main
```

Single-location mode:

```powershell
python -m weather_logistics_system.main --location "London"
```

Multiple locations:

```powershell
python -m weather_logistics_system.main --location "London,New York,Tokyo"
```

## Graph Output

Charts are saved here:

```text
assignment 5.1/outputs/
```

Example command-line output:

```text
Visualization Agent: chart saved to:
C:\Users\Dan\Documents\Codex\Agentic-Learning-Course\assignment 5.1\outputs\temperature_trends_london.png
```

This gives you a file you can include as a screenshot or direct artifact for the
graphs deliverable.

## Step 4: Test the System

Test with at least three locations:

```text
London
New York
Tokyo
```

Verify that:

- The Data Gathering Agent fetches forecast data.
- The Data Processing Agent provides actionable logistics insights.
- The Visualization Agent saves clear PNG charts in `outputs/`.

## Deliverables

- Python code: submit the complete implementation.
- Generated insights: provide outputs for three different locations.
- Graphs: include screenshots or PNG files from the `outputs/` directory.
- Reflection report: discuss how each agent contributes to the system and
  describe challenges.
- Reflection questions:
  - How does collaboration between three agents improve the system's efficiency?
  - What challenges did you face in integrating the agents?
  - How could this system be extended for other use cases, such as financial
    analysis?

## Project Structure

```text
assignment 5.1/
  outputs/
  pyproject.toml
  requirements.txt
  src/
    weather_logistics_system/
      __init__.py
      agents.py
      main.py
```
