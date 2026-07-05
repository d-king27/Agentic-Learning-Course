from __future__ import annotations

import argparse

from feedback_reflection.agent import ReflectiveFeedbackAgent


CUSTOMER_FEEDBACK = (
    "The delivery was late, and the packaging was damaged. However, the customer "
    "service team was very helpful in resolving the issue."
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the reflective feedback agent.")
    parser.add_argument(
        "--iterations",
        type=int,
        default=3,
        help="Number of reflection iterations to run.",
    )
    args = parser.parse_args()

    agent = ReflectiveFeedbackAgent()
    results = agent.run(CUSTOMER_FEEDBACK, iterations=args.iterations)

    print("Customer feedback:")
    print(CUSTOMER_FEEDBACK)

    for result in results:
        print(f"\n--- Iteration {result.iteration} ---")
        print("\nAnalysis:")
        print(result.analysis)
        print("\nRefined analysis:")
        print(result.refined_analysis)

    print("\nFinal refined analysis:")
    print(results[-1].refined_analysis)


if __name__ == "__main__":
    main()
