"""
v5: Self-critique. Generate -> critique -> refine pattern.
"""

import re
from llm import call


GENERATE_SYSTEM = """
You are a math problem solver.
Reason step by step inside <reasoning>...</reasoning>,
then give the final integer in <answer>...</answer>.
"""


CRITIQUE_SYSTEM = """
You are a meticulous math reviewer.

Given a problem and a proposed solution, identify any errors in:
- Setup (did they read the problem correctly?)
- Arithmetic (any calculation mistakes?)
- Logic (does each step follow correctly?)
- Answer (does it match the question?)

Be specific. If correct, say so.

Reply in this format:
<issues>
[List issues OR "None — solution looks correct."]
</issues>
<verdict>correct or incorrect</verdict>
"""


REFINE_SYSTEM = """
You are a math problem solver revising your previous answer.

You will receive:
- problem
- previous solution
- review feedback

Fix all issues and produce a corrected solution.

Reason step by step inside <reasoning>...</reasoning>,
then give the final integer in <answer>...</answer>.
"""


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


def parse_verdict(text: str) -> str:

    match = re.search(
        r"<verdict>\s*(\w+)\s*</verdict>",
        text,
        re.IGNORECASE
    )

    return match.group(1).lower() if match else "unknown"


def solve(question: str) -> dict:
    """
    Generate -> critique -> refine.
    """

    # Step 1: Generate
    initial = call(
        prompt=question,
        system=GENERATE_SYSTEM,
        temperature=0.0,
        max_tokens=1024,
    )

    # Step 2: Critique
    critique_prompt = (
        f"Problem: {question}\n\n"
        f"Solution:\n{initial}\n\n"
        f"Review it carefully."
    )

    critique = call(
        prompt=critique_prompt,
        system=CRITIQUE_SYSTEM,
        temperature=0.0,
        max_tokens=512,
    )

    verdict = parse_verdict(critique)

    # Step 3: If correct, return directly
    if verdict == "correct":
        return {
            "answer": parse_answer(initial),
            "iterations": 1,
            "verdict": verdict,
        }

    # Step 4: Refine
    refine_prompt = (
        f"Problem: {question}\n\n"
        f"Previous solution:\n{initial}\n\n"
        f"Feedback:\n{critique}\n\n"
        f"Now fix the solution."
    )

    refined = call(
        prompt=refine_prompt,
        system=REFINE_SYSTEM,
        temperature=0.0,
        max_tokens=1024,
    )

    return {
        "answer": parse_answer(refined),
        "iterations": 2,
        "verdict": verdict,
    }


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
            "iterations": r["iterations"],
        })

        print(
            f"{p['id']} ({p['difficulty']}): "
            f"got {r['answer']} (iters={r['iterations']}, "
            f"verdict={r['verdict']}) expected {p['answer']} "
            f"{'OK' if correct else 'FAIL'}"
        )

    return results


if __name__ == "__main__":

    print("=== v5: Self-Critique ===")

    results = run_all()

    correct = sum(1 for r in results if r["correct"])
    refined_count = sum(1 for r in results if r["iterations"] > 1)

    print(
        f"\nAccuracy: {correct}/{len(results)} = "
        f"{correct/len(results)*100:.0f}%"
    )

    print(
        f"Refined (critique triggered): "
        f"{refined_count}/{len(results)}"
    )