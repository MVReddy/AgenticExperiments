"""Harvey-style Q&A agent (inspired by Harvey AI).

Simulates: an assistant that answers legal questions with a confidence
score and cited sources, warning the user when confidence drops below 70%.

Run:
    python experiments/03_harvey_style_qa.py --question "What is consideration?"

CHALLENGE: Add a follow-up mode that asks clarifying questions when confidence < 50%.
"""
from __future__ import annotations

import argparse

KNOWLEDGE: dict[str, tuple[str, int, list[str]]] = {
    "consideration": (
        "Consideration is something of value exchanged between parties "
        "that makes a promise enforceable.",
        92,
        ["Restatement (Second) of Contracts \u00a7 71"],
    ),
    "negligence": (
        "Negligence requires duty, breach, causation, and damages.",
        88,
        ["Restatement (Third) of Torts \u00a7 3"],
    ),
    "hearsay": (
        "Hearsay is an out-of-court statement offered for the truth "
        "of the matter asserted.",
        81,
        ["Fed. R. Evid. 801(c)"],
    ),
}


class HarveyAgent:
    CONFIDENCE_FLOOR = 70

    def ask(self, question: str) -> dict:
        q = question.lower()
        for key, (answer, conf, sources) in KNOWLEDGE.items():
            if key in q:
                return self._package(answer, conf, sources)
        return self._package(
            "I don't have a reliable answer for that in my knowledge base.",
            35,
            [],
        )

    def _package(self, answer: str, confidence: int, sources: list[str]) -> dict:
        warning = ""
        if confidence < self.CONFIDENCE_FLOOR:
            warning = (f"WARNING: low confidence ({confidence}% < "
                       f"{self.CONFIDENCE_FLOOR}%) -- verify with primary "
                       "sources before relying on this.")
        return {"answer": answer, "confidence": confidence,
                "sources": sources, "warning": warning}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", default="What is consideration in contract law?")
    args = parser.parse_args()
    result = HarveyAgent().ask(args.question)
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Sources: {', '.join(result['sources']) or 'none'}")
    if result["warning"]:
        print(result["warning"])


if __name__ == "__main__":
    main()
