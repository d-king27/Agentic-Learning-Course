from __future__ import annotations

import argparse

from multi_agent_stock_system.agents import MultiAgentStockSystem


def print_result(symbol: str, system: MultiAgentStockSystem) -> None:
    print(f"\nStarting multi-agent system for {symbol.upper()}...\n")
    summary, chart, insights = system.run(symbol)

    print("\nData Summary:")
    print(summary.to_prompt_text())

    print("\nRecent Price Chart:")
    print(chart)

    print("\nGenerated Insights:")
    print(insights)


def run_interactive(system: MultiAgentStockSystem) -> None:
    print("Welcome to the Multi-Agent Stock System!")
    print("Type 'exit' to quit.\n")

    while True:
        symbol = input("Enter a stock symbol (e.g., AAPL, TSLA): ").strip()

        if symbol.lower() == "exit":
            print("Goodbye!")
            break

        try:
            print_result(symbol, system)
        except RuntimeError as error:
            print(f"\nError: {error}")

        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the multi-agent stock system.")
    parser.add_argument(
        "--symbol",
        help="Stock symbol, or comma-separated stock symbols, such as AAPL or AAPL,MSFT.",
    )
    args = parser.parse_args()

    system = MultiAgentStockSystem()

    if args.symbol:
        symbols = [symbol.strip() for symbol in args.symbol.split(",") if symbol.strip()]

        for symbol in symbols:
            try:
                print_result(symbol, system)
            except RuntimeError as error:
                print(f"\nError for {symbol.upper()}: {error}")
        return

    run_interactive(system)


if __name__ == "__main__":
    main()

