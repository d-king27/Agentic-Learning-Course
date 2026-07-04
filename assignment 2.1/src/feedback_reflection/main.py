from __future__ import annotations

from feedback_reflection.agent import ReflectiveFeedbackAgent


CUSTOMER_FEEDBACK = (
    "The delivery was late, and the packaging was damaged. However, the customer "
    "service team was very helpful in resolving the issue."
)


def main() -> None:
    agent = ReflectiveFeedbackAgent()
    results = agent.run(CUSTOMER_FEEDBACK, iterations=3)

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

