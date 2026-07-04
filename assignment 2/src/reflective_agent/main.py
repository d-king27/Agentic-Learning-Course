from __future__ import annotations

from reflective_agent.agent import ReflectiveCodeAgent


STARTING_CODE = """
def sum_numbers(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total
""".strip()


def main() -> None:
    agent = ReflectiveCodeAgent()
    results = agent.improve(STARTING_CODE, rounds=2)

    print("Starting code:")
    print(STARTING_CODE)

    for result in results:
        print(f"\n--- Reflection round {result.round_number} ---")
        print("\nAnalysis:")
        print(result.analysis)
        print("\nRefined analysis:")
        print(result.refined_analysis)
        print("\nRevised code:")
        print(result.revised_code)


if __name__ == "__main__":
    main()
