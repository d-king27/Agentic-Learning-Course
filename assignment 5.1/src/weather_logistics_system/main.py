from __future__ import annotations

import argparse

from weather_logistics_system.agents import WeatherLogisticsSystem


def print_result(location: str, system: WeatherLogisticsSystem) -> None:
    print(f"\nStarting multi-agent system for {location}...\n")
    summary, chart_path, insights = system.run(location)

    print("\nForecast Summary:")
    print(summary.to_prompt_text())

    print("\nGenerated Insights:")
    print(insights)

    print("\nGraph Output:")
    print(f"Temperature chart saved to: {chart_path}")


def run_interactive(system: WeatherLogisticsSystem) -> None:
    print("Welcome to the Multi-Agent Weather Logistics System!")
    print("Type 'exit' to quit.\n")

    while True:
        location = input("Enter a location (e.g., New York, Tokyo): ").strip()

        if location.lower() == "exit":
            print("Goodbye!")
            break

        try:
            print_result(location, system)
        except RuntimeError as error:
            print(f"\nError: {error}")

        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the multi-agent weather logistics system."
    )
    parser.add_argument(
        "--location",
        help="Location, or comma-separated locations, such as London or London,Tokyo.",
    )
    args = parser.parse_args()

    system = WeatherLogisticsSystem()

    if args.location:
        locations = [
            location.strip() for location in args.location.split(",") if location.strip()
        ]

        for location in locations:
            try:
                print_result(location, system)
            except RuntimeError as error:
                print(f"\nError for {location}: {error}")
        return

    run_interactive(system)


if __name__ == "__main__":
    main()

