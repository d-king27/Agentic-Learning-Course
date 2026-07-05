from __future__ import annotations

import argparse

from stock_market_advisor.agent import StockMarketAdvisorAgent


def print_result(symbol: str, agent: StockMarketAdvisorAgent) -> None:
    print(f"\nFetching stock data for {symbol.upper()}...")
    stock_analysis, recommendation = agent.run(symbol)

    print("\nStock analysis:")
    print(stock_analysis.to_prompt_text())

    print("\nRecommendation:")
    print(recommendation)


def run_interactive(agent: StockMarketAdvisorAgent) -> None:
    print("Welcome to the Stock Market Advisor!")
    print("Type 'exit' to quit.\n")

    while True:
        symbol = input("Enter a stock symbol (e.g., AAPL, TSLA): ").strip()

        if symbol.lower() == "exit":
            print("Goodbye!")
            break

        try:
            print_result(symbol, agent)
        except RuntimeError as error:
            print(f"\nError: {error}")

        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the stock market advisor agent.")
    parser.add_argument(
        "--symbol",
        help="Stock symbol, or comma-separated stock symbols, such as AAPL or AAPL,TSLA.",
    )
    args = parser.parse_args()

    agent = StockMarketAdvisorAgent()

    if args.symbol:
        symbols = [symbol.strip() for symbol in args.symbol.split(",") if symbol.strip()]

        for symbol in symbols:
            try:
                print_result(symbol, agent)
            except RuntimeError as error:
                print(f"\nError for {symbol.upper()}: {error}")
        return

    run_interactive(agent)


if __name__ == "__main__":
    main()

