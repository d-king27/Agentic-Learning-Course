from __future__ import annotations

import argparse

from weather_recommendation.agent import WeatherRecommendationAgent


def print_result(location: str, preference: str, agent: WeatherRecommendationAgent) -> None:
    print(f"\nFetching weather data for {location}...")
    weather_report, recommendations = agent.run(location, preference)

    print("\nWeather summary:")
    print(weather_report.to_prompt_text())

    print("\nRecommendations:")
    print(recommendations)


def run_interactive(agent: WeatherRecommendationAgent) -> None:
    print("Welcome to the Weather Recommendation Agent!")
    print("Type 'exit' to quit.\n")

    while True:
        location = input("Enter your city: ").strip()

        if location.lower() == "exit":
            print("Goodbye!")
            break

        preference = input(
            "Any preference? Example: outdoor activities, travel safety tips, or press Enter: "
        ).strip()
        preference = preference or "general recommendations"

        try:
            print_result(location, preference, agent)
        except RuntimeError as error:
            print(f"\nError: {error}")

        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the weather recommendation agent.")
    parser.add_argument("--city", help="City to fetch weather for.")
    parser.add_argument(
        "--preference",
        default="general recommendations",
        help="Optional preference, such as outdoor activities or travel safety tips.",
    )
    args = parser.parse_args()

    agent = WeatherRecommendationAgent()

    if args.city:
        print_result(args.city, args.preference, agent)
        return

    run_interactive(agent)


if __name__ == "__main__":
    main()

