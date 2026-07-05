from __future__ import annotations

import argparse

from meal_prep_planner.agent import MealPreferences, MealPrepPlannerAgent


def parse_optional_int(value: str) -> int | None:
    value = value.strip()

    if not value:
        return None

    return int(value)


def collect_meal_preferences() -> MealPreferences | None:
    print("\nLet's create your meal preparation plan!")
    meal_type = input("Type of meal, such as breakfast, lunch, or dinner: ").strip()

    if meal_type.lower() == "exit":
        return None

    dietary = input(
        "Dietary preferences or restrictions, such as vegetarian or gluten-free: "
    ).strip()
    servings = int(input("Number of servings: ").strip())
    cooking_time = parse_optional_int(
        input("Available cooking time in minutes, or press Enter: ")
    )
    allergies = input("Any allergies or ingredients to avoid? Press Enter if none: ").strip()
    extra_preferences = input(
        "Any extra preferences, such as high protein or budget-friendly? Press Enter if none: "
    ).strip()

    return MealPreferences(
        meal_type=meal_type,
        dietary_preferences=dietary or "No specific dietary restrictions",
        servings=servings,
        cooking_time_minutes=cooking_time,
        allergies=allergies or "None",
        extra_preferences=extra_preferences or "None",
    )


def print_plan(plan: str) -> None:
    print("\nGenerated meal preparation plan:\n")
    print(plan)


def run_interactive(agent: MealPrepPlannerAgent) -> None:
    print("Welcome to the Meal Preparation Planning Agent!")
    print("Type 'exit' at the meal type prompt to quit.\n")

    while True:
        meal_preferences = collect_meal_preferences()

        if meal_preferences is None:
            print("Goodbye!")
            break

        print("\nGenerating your meal plan...")
        plan = agent.generate_plan(meal_preferences)
        print_plan(plan)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the meal preparation planner.")
    parser.add_argument("--meal-type", help="Type of meal, such as breakfast or dinner.")
    parser.add_argument("--dietary", help="Dietary preferences or restrictions.")
    parser.add_argument("--servings", type=int, help="Number of servings.")
    parser.add_argument("--time", type=int, help="Available cooking time in minutes.")
    parser.add_argument("--allergies", default="None", help="Allergies or ingredients to avoid.")
    parser.add_argument("--preferences", default="None", help="Extra meal preferences.")
    args = parser.parse_args()

    agent = MealPrepPlannerAgent()

    if args.meal_type or args.dietary or args.servings:
        missing = [
            name
            for name, value in {
                "--meal-type": args.meal_type,
                "--dietary": args.dietary,
                "--servings": args.servings,
            }.items()
            if not value
        ]

        if missing:
            raise RuntimeError(f"Missing required arguments: {', '.join(missing)}")

        meal_preferences = MealPreferences(
            meal_type=args.meal_type,
            dietary_preferences=args.dietary,
            servings=args.servings,
            cooking_time_minutes=args.time,
            allergies=args.allergies,
            extra_preferences=args.preferences,
        )
        print("\nGenerating your meal plan...")
        plan = agent.generate_plan(meal_preferences)
        print_plan(plan)
        return

    run_interactive(agent)


if __name__ == "__main__":
    main()

