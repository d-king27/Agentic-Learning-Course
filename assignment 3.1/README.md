# Assignment 3.1: Stock Market Advisor Agent

Objective: build an AI agent that integrates an external stock market API for
dynamic problem-solving.

The agent accepts a stock symbol, fetches daily market data from Alpha Vantage,
analyzes recent performance, and uses a language model to generate a clear
buy/sell/hold-style recommendation.

This project is for learning purposes only and does not provide personal
financial advice.

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

Add your stock market API key:

```text
STOCK_MARKET_API_KEY="your-alpha-vantage-api-key-here"
```

This is the single source of truth for the Alpha Vantage key in this project.

The OpenAI key is also loaded from the same file:

```text
OPEN_AI_KEY="your-openai-api-key-here"
OPENAI_MODEL="gpt-4"
```

## Step 3: Understand the Workflow

```text
1. Accept a stock symbol from the user.
2. Fetch daily stock data from Alpha Vantage.
3. Extract recent prices and volume.
4. Analyze the latest close, daily change, five-day change, and volume trend.
5. Send the compact analysis to the language model.
6. Generate a recommendation with a short rationale and risk notes.
```

## Step 4: Run the Agent

Interactive mode:

```powershell
python -m stock_market_advisor.main
```

Single-symbol mode:

```powershell
python -m stock_market_advisor.main --symbol AAPL
```

Multi-symbol mode:

```powershell
python -m stock_market_advisor.main --symbol AAPL,TSLA,MSFT
```

## Step 5: Test Your Agent

Test at least three symbols and save the outputs for the sample runs
deliverable.

Example symbols:

```text
AAPL
TSLA
MSFT
```

## Deliverables

- Python script: submit the full code for the agent.
- Sample runs: include outputs for at least three stock symbols.
- Reflection report: describe how tool integration enhanced the agent and what
  challenges came up during implementation.
- Reflection questions:
  - How did integrating the stock API improve the AI's real-world applicability?
  - What insights did the AI generate that were enhanced by the external tool?
  - How could this agent be extended with multi-day forecasts or news sentiment
    analysis?

## Project Structure

```text
assignment 3.1/
  pyproject.toml
  requirements.txt
  src/
    stock_market_advisor/
      __init__.py
      agent.py
      main.py
```
