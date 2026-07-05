# Assignment 5: Multi-Agent Data Gathering and Processing System

Objective: build a multi-agent system where one agent gathers external data and
another agent processes that data into actionable insights.

This assignment uses Alpha Vantage stock data as the external API source. The
system includes:

- Data Gathering Agent: fetches intraday stock data.
- Data Processing Agent: analyzes the gathered data and generates insights.
- Visualization Agent: creates a simple text chart from recent prices.

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
STOCK_MARKET_API_KEY="your-alpha-vantage-api-key-here"
```

## Step 2: Design the System Workflow

```text
1. User enters a stock symbol.
2. Data Gathering Agent fetches intraday stock data from Alpha Vantage.
3. Data Processing Agent extracts recent prices, volume, and trend signals.
4. Data Processing Agent sends a compact summary to the language model.
5. Visualization Agent creates a simple text chart of recent closing prices.
6. The system displays the insight, recommendation, and chart.
```

## Step 3: Run the System

Interactive mode:

```powershell
python -m multi_agent_stock_system.main
```

Single-symbol mode:

```powershell
python -m multi_agent_stock_system.main --symbol AAPL
```

Multi-symbol mode:

```powershell
python -m multi_agent_stock_system.main --symbol AAPL,MSFT,TSLA
```

## Step 4: Test the System

Test at least three symbols and save the output for the sample outputs
deliverable.

Example symbols:

```text
AAPL
MSFT
TSLA
```

## Deliverables

- Python script: submit the full implementation.
- Sample outputs: include at least three example runs with different stock
  symbols.
- Reflection: explain how the data gathering and processing agents interact,
  and describe the value of multi-agent collaboration.
- Reflection questions:
  - How does dividing the tasks between two agents improve efficiency and
    clarity?
  - What challenges did you encounter during data integration?
  - How could this system be extended to support more complex analysis or
    additional data sources?

## Project Structure

```text
assignment 5/
  pyproject.toml
  requirements.txt
  src/
    multi_agent_stock_system/
      __init__.py
      agents.py
      main.py
```
