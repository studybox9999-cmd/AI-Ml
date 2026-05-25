"""
v3: Few-shot CoT. We include 3 worked examples to demonstrate the EXACT
reasoning style we want.
"""

import re
from llm import call


SYSTEM = """
You are a careful math problem solver.
Reason step by step inside <reasoning>...</reasoning>,
then give the final integer in <answer>...</answer>.
"""


# Three worked examples, chosen to be SIMILAR IN STYLE
# but not identical to any of the real problems.
FEW_SHOT_EXAMPLES = """
Here are examples of the format I want:

Question: Lisa bought 4 packs of pens. Each pack has 6 pens. She gave 1/3 of the
pens to her sister. How many pens does she have left?
<reasoning>
Total pens = 4 * 6 = 24.
She gave away 1/3 = 8.
Remaining = 24 - 8 = 16.
</reasoning>
<answer>16</answer>

Question: A water tank holds 200 liters. It is 3/4 full. A pipe drains 25 liters
per hour. After how many hours will the tank be empty?
<reasoning>
Current water = 200 * 3/4 = 150.
Drain rate = 25 per hour.
Time = 150 / 25 = 6.
</reasoning>
<answer>6</answer>

Question: Two friends split a $48 bill. The first friend's meal cost $4 more than
half the bill. How much did the second friend's meal cost?
<reasoning>
Half = 24.
First friend = 24 + 4 = 28.
Second friend = 48 - 28 = 20.
</reasoning>
<answer>20</answer>

Now solve the next question in the same format.
"""


def solve(question: str) -> dict:

    prompt = f"{FEW_SHOT_EXAMPLES}\n\nQuestion: {question}"

    response = call(
        prompt=prompt,
        system=SYSTEM,
        temperature=0.0,
        max_tokens=1024,
    )

    answer = parse_answer(response)

    return {
        "answer": answer,
        "raw": response
    }


def parse_answer(text: str) -> int | None:

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

    print("=== v3: Few-Shot CoT ===")

    results = run_all()

    correct = sum(1 for r in results if r["correct"])

    print(
        f"\nAccuracy: {correct}/{len(results)} = "
        f"{correct/len(results)*100:.0f}%"
    )