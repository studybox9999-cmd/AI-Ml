"""
v1: Baseline solver.
No CoT, no reasoning scaffolding.
Just: question -> answer.
"""

import re
from llm import call


SYSTEM = """
You are a math problem solver.
Read the problem and provide ONLY
the final numerical answer.

Do not show your work.
Do not explain.
Reply with just an integer.
"""


def solve(question: str) -> dict:
    """
    Solve a single problem.

    Return:
    {
        "answer": int | None,
        "raw": str
    }
    """

    response = call(
        prompt=question,
        system=SYSTEM,
        temperature=0.0,
        max_tokens=50,
    )

    answer = parse_answer(response)

    return {
        "answer": answer,
        "raw": response
    }


def parse_answer(text: str) -> int | None:
    """
    Extract an integer from response.
    Return None if not found.
    """

    match = re.search(
        r"-?\d+",
        text.replace(",", "")
    )

    if match:
        try:
            return int(match.group())
        except ValueError:
            return None

    return None


def run_all():
    """
    Run full benchmark on all problems.
    """
    from problems import get_problems

    problems = get_problems()

    results = []

    for p in problems:
        result = solve(p["question"])

        output = {
            "question": p["question"],
            "predicted": result["answer"],
            "expected": p["answer"],
            "raw": result["raw"]
        }

        print(f"Q: {output['question']}")
        print(f"A: {output['predicted']} (expected {output['expected']})")
        print(f"Raw: {output['raw']}")
        print("-" * 40)

        results.append(output)

    return results


if __name__ == "__main__":

    # Quick smoke test
    run_all()