# Assignment 6: Unified Customer Support Agentic System

Objective: build a unified customer support system that combines Tool Use,
Planning, Reflection, and Multi-Agent patterns.

The system simulates a customer support API, retrieves customer issue data,
generates a resolution plan, refines that plan, and returns a final
support-ready output.

## Scenario

Customer Support System:

- Automates support triage.
- Reduces response time.
- Produces consistent resolution plans.
- Handles missing customer records gracefully.

## Agent Architecture

```text
Customer ID
  -> Tool Use Agent fetches customer data
  -> Planning Agent creates an initial resolution plan
  -> Reflection Agent critiques and refines the plan
  -> Orchestrator returns the final support-ready output
```

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

## Step 2: Run the System

Interactive mode:

```powershell
python -m customer_support_system.main
```

Single-customer mode:

```powershell
python -m customer_support_system.main --customer-id 123
```

Multiple customers:

```powershell
python -m customer_support_system.main --customer-id 123,456,789
```

Test fallback handling:

```powershell
python -m customer_support_system.main --customer-id 999
```

## Sample Customer IDs

```text
123 - Alice - Payment not processed - High priority
456 - Bob - Unable to log in - Medium priority
789 - Priya - Order not delivered - High priority
321 - Marcus - Subscription cancellation - Low priority
```

## Deliverables

- Python script: submit the full implementation.
- Sample outputs: include successful support cases and one fallback/error case.
- Architecture explanation: describe how the agents interact.
- Reflection report: evaluate efficiency, scalability, and adaptability.
- Reflection questions:
  - How does combining Tool Use, Planning, Reflection, and Multi-Agent patterns
    improve the system?
  - How does the simulated API support the Tool Use pattern?
  - How could this system connect to a real support platform?

## Project Structure

```text
assignment 6/
  pyproject.toml
  requirements.txt
  src/
    customer_support_system/
      __init__.py
      agents.py
      main.py
```
