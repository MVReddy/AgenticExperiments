"""Daily challenge generator for AgenticExperiments.

Picks 3 of 12 hands-on challenges deterministically from today's date,
so everyone playing on the same day gets the same set.

Run:
    python experiments/10_daily_challenge.py [--seed YYYY-MM-DD]

CHALLENGE: Track your completions in a local JSON streak file.
"""
from __future__ import annotations

import argparse
import random
from datetime import date

CHALLENGES = [
    "01: Add citation-checking to the Protege research agent.",
    "02: Make CoCounsel's verifier catch fake pin cites.",
    "03: Give Harvey a clarifying-question mode under 50% confidence.",
    "04: Export Legora's grid to CSV.",
    "05: Add a liability-cap clause to the Luminance negotiation.",
    "06: Teach Spellbook's reviewer to suggest fix language.",
    "07: Add a parallel Critic agent to the CrewAI crew.",
    "08: Add a draft -> research retry loop to the LangGraph workflow.",
    "09: Add a deadline-checking tool to the smolagents agent.",
    "10: Build a simple CLI menu to run any experiment.",
    "11: Benchmark two prompting strategies on the same task.",
    "12: Write a 5-question quiz testing what you learned this week.",
]


def pick_challenges(seed: str, n: int = 3) -> list[str]:
    rng = random.Random(seed)
    return rng.sample(CHALLENGES, n)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", default=date.today().isoformat())
    args = parser.parse_args()
    print(f"Today's challenges ({args.seed}):\n")
    for i, challenge in enumerate(pick_challenges(args.seed), 1):
        print(f"  {i}. {challenge}")
    print("\nShare your solutions -- commit them and keep the streak alive!")


if __name__ == "__main__":
    main()
