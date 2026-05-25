"""
v2: Zero-shot CoT. The single most important change in this entire lab.
"""

import re
from llm import call


SYSTEM = """
You are a careful math problem solver.

For every problem:
1. Reason step by step inside <reasoning>...</reasoning> tags.
2. Then provide the final integer answer inside <answer>...</answer> tags.

Always show your work. Always end with the answer in tags.
"""


def solve(question: str) -> dict:
    response = call(
        prompt=question,
        system=SYSTEM,
        temperature=0.0,
        max_tokens=1024,  # Need more tokens — CoT generates reasoning
    )

    answer = parse_answer(response)

    return {
        "answer": answer,
        "raw": response
    }


def parse_answer(text: str) -> int | None:
    """Extract integer from <answer>...</answer> tags."""

    match = re.search(
        r"<answer>\s*(-?\d[\d,]*)\s*</answer>",
        text,
        re.IGNORECASE
    )

    if match:
        try:
            return int(match.group(1).replace(",", ""))
        except ValueError:
            return None

    # Fallback: last integer in response
    nums = re.findall(r"-?\d+", text.replace(",", ""))
    return int(nums[-1]) if nums else None


def run_all() -> list[dict]:

    from problems import get_problems

    results = []

    for p in get_problems():

        r = solve(p["question"])
        correct = (r["answer"] == p["answer"])

        results.append({
            "id": p["id"],
            "difficulty": p["difficulty"],
            "expected": p["answer"],
            "got": r["answer"],
            "correct": correct,
        })

        print(
            f"{p['id']} ({p['difficulty']}): "
            f"got {r['answer']}, expected {p['answer']} "
            f"{'OK' if correct else 'FAIL'}"
        )

    return results


if __name__ == "__main__":

    print("=== v2: Zero-Shot CoT ===")

    results = run_all()

    correct = sum(1 for r in results if r["correct"])

    print(
        f"\nAccuracy: {correct}/{len(results)} = "
        f"{correct/len(results)*100:.0f}%"
    )