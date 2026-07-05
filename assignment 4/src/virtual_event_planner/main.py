from __future__ import annotations

import argparse

from virtual_event_planner.agent import EventDetails, VirtualEventPlannerAgent


def print_plan(event_plan: str, checklist: list[dict[str, str]]) -> None:
    print("\nHere is your event plan:\n")
    print(event_plan)

    if not checklist:
        return

    print("\nProgress checklist:\n")

    for index, item in enumerate(checklist, start=1):
        print(f"[ ] {index}. {item['phase']}: {item['task']}")


def track_progress(checklist: list[dict[str, str]]) -> None:
    if not checklist:
        return

    completed: set[int] = set()

    while True:
        choice = input(
            "\nEnter a task number to mark complete, 'status' to view progress, or 'done': "
        ).strip()

        if choice.lower() == "done":
            break

        if choice.lower() == "status":
            show_status(checklist, completed)
            continue

        if not choice.isdigit():
            print("Please enter a task number, 'status', or 'done'.")
            continue

        task_number = int(choice)

        if task_number < 1 or task_number > len(checklist):
            print("That task number is not in the checklist.")
            continue

        completed.add(task_number)
        item = checklist[task_number - 1]
        print(f"Marked complete: {item['phase']}: {item['task']}")

    show_status(checklist, completed)


def show_status(checklist: list[dict[str, str]], completed: set[int]) -> None:
    print("\nCurrent progress:\n")

    for index, item in enumerate(checklist, start=1):
        marker = "x" if index in completed else " "
        print(f"[{marker}] {index}. {item['phase']}: {item['task']}")


def collect_event_details() -> EventDetails | None:
    print("\nLet's plan your virtual event!")
    event_type = input("What type of event are you organizing? ").strip()

    if event_type.lower() == "exit":
        return None

    date = input("What is the date of the event? ").strip()
    audience = input("Who is the target audience? ").strip()
    goals = input("What are the main goals of the event? ").strip()

    return EventDetails(
        event_type=event_type,
        date=date,
        audience=audience,
        goals=goals,
    )


def run_interactive(agent: VirtualEventPlannerAgent) -> None:
    print("Welcome to the Virtual Event Planning Agent!")
    print("Type 'exit' at the event type prompt to quit.\n")

    while True:
        event_details = collect_event_details()

        if event_details is None:
            print("Goodbye!")
            break

        print("\nGenerating the event plan...")
        event_plan, checklist = agent.run(event_details)
        print_plan(event_plan, checklist)
        track_progress(checklist)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the virtual event planning agent.")
    parser.add_argument("--type", help="Event type, such as webinar or workshop.")
    parser.add_argument("--date", help="Event date.")
    parser.add_argument("--audience", help="Target audience.")
    parser.add_argument("--goals", help="Main event goals.")
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Skip interactive progress tracking after the plan is generated.",
    )
    args = parser.parse_args()

    agent = VirtualEventPlannerAgent()

    if args.type or args.date or args.audience or args.goals:
        missing = [
            name
            for name, value in {
                "--type": args.type,
                "--date": args.date,
                "--audience": args.audience,
                "--goals": args.goals,
            }.items()
            if not value
        ]

        if missing:
            raise RuntimeError(f"Missing required arguments: {', '.join(missing)}")

        event_details = EventDetails(
            event_type=args.type,
            date=args.date,
            audience=args.audience,
            goals=args.goals,
        )
        print("\nGenerating the event plan...")
        event_plan, checklist = agent.run(event_details)
        print_plan(event_plan, checklist)

        if not args.no_progress:
            track_progress(checklist)

        return

    run_interactive(agent)


if __name__ == "__main__":
    main()

