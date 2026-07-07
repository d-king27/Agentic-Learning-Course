from __future__ import annotations

import argparse

from customer_support_system.agents import CustomerSupportOrchestrator


def print_result(customer_id: str, orchestrator: CustomerSupportOrchestrator) -> None:
    result = orchestrator.run(customer_id)

    if result.error:
        print("\nError / Fallback:")
        print(result.error)
        return

    if result.customer_record:
        print("\nCustomer Data:")
        print(result.customer_record.to_prompt_text())

    print("\nInitial Resolution Plan:")
    print(result.initial_plan)

    print("\nRefined Resolution Plan:")
    print(result.refined_plan)

    print("\nFinal Output:")
    print(result.refined_plan)


def run_interactive(orchestrator: CustomerSupportOrchestrator) -> None:
    print("Welcome to the Unified Customer Support System!")
    print("Type 'exit' to quit.\n")

    while True:
        customer_id = input("Enter Customer ID (e.g., 123, 456): ").strip()

        if customer_id.lower() == "exit":
            print("Goodbye!")
            break

        print_result(customer_id, orchestrator)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the unified customer support agentic system."
    )
    parser.add_argument(
        "--customer-id",
        help="Customer ID, or comma-separated customer IDs, such as 123 or 123,456.",
    )
    args = parser.parse_args()

    orchestrator = CustomerSupportOrchestrator()

    if args.customer_id:
        customer_ids = [
            customer_id.strip()
            for customer_id in args.customer_id.split(",")
            if customer_id.strip()
        ]

        for customer_id in customer_ids:
            print_result(customer_id, orchestrator)
            print()
        return

    run_interactive(orchestrator)


if __name__ == "__main__":
    main()

