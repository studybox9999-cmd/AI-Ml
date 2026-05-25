"""
Run all variants on the same problem set and produce comparison table.
"""

from tabulate import tabulate
import llm

import v1_baseline
import v2_zero
import v3_zero
import v4_self
import v5_selfC


VARIANTS = [
    ("v1 Baseline", v1_baseline),
    ("v2 Zero-Shot CoT", v2_zero),
    ("v3 Few-Shot CoT", v3_zero),
    ("v4 Self-Consistency", v4_self),
    ("v5 Self-Critique", v5_selfC),
]


def main():

    summary_rows = []

    for name, module in VARIANTS:

        print("\n" + "=" * 60)
        print(f"Running {name}...")
        print("=" * 60)

        llm.reset_usage()
        results = module.run_all()
        usage = llm.get_usage()

        correct = sum(1 for r in results if r.get("correct", False))
        total = len(results)

        easy_correct = sum(
            1 for r in results
            if r.get("correct") and r.get("difficulty") == "easy"
        )

        med_correct = sum(
            1 for r in results
            if r.get("correct") and r.get("difficulty") == "medium"
        )

        hard_correct = sum(
            1 for r in results
            if r.get("correct") and r.get("difficulty") == "hard"
        )

        cost = (
            usage.get("input_tokens", 0) * 3.00 +
            usage.get("output_tokens", 0) * 15.00
        ) / 1_000_000

        summary_rows.append([
            name,
            f"{correct}/{total}",
            f"{(correct/total*100) if total else 0:.0f}%",
            f"{easy_correct}",
            f"{med_correct}",
            f"{hard_correct}",
            usage.get("input_tokens", 0),
            usage.get("output_tokens", 0),
            f"${cost:.4f}",
        ])

    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    print(
        tabulate(
            summary_rows,
            headers=[
                "Variant",
                "Score",
                "Accuracy",
                "Easy",
                "Medium",
                "Hard",
                "Input Tokens",
                "Output Tokens",
                "Cost"
            ],
            tablefmt="grid"
        )
    )


if __name__ == "__main__":
    main()