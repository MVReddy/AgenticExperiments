"""Protege-style research loop (inspired by LexisNexis Protege).

Simulates a legal research agent: private Vault, multi-step tasking,
prompt-refinement suggestions, draft memo, and self-review.
Run: python experiments/01_protege_style_research_agent.py --query "force majeure"

CHALLENGE: Add a citation-checker flagging quotes not present in the Vault.
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass


@dataclass
class Document:
    title: str
    text: str


class Vault:
    """Private document store, like Protege's Vault."""

    def __init__(self) -> None:
        self._docs: list[Document] = []

    def add(self, title: str, text: str) -> None:
        self._docs.append(Document(title, text))

    def search(self, query: str, top_k: int = 3) -> list[Document]:
        terms = set(re.findall(r"\w+", query.lower()))

        def score(doc: Document) -> int:
            return len(terms & set(re.findall(r"\w+", doc.text.lower())))

        ranked = sorted(self._docs, key=score, reverse=True)
        return [d for d in ranked[:top_k] if score(d) > 0]


class ProtegeAgent:
    """Multi-step research agent with self-review."""

    def __init__(self, vault: Vault) -> None:
        self.vault = vault

    def suggest_prompt_refinement(self, query: str) -> str:
        if len(query.split()) < 4:
            return f'"{query}" -> try: "{query} legal standard elements burden of proof"'
        return f'"{query}" looks well-formed. Consider adding a jurisdiction.'

    def summarize_doc(self, doc: Document, max_chars: int = 160) -> str:
        return f"[{doc.title}] {doc.text[:max_chars].strip()}..."

    def _draft_memo(self, query: str, docs: list[Document]) -> str:
        body = "\n".join(f"- {self.summarize_doc(d)}" for d in docs)
        return f"MEMO -- Re: {query}\n\n{body}"

    def _self_review(self, memo: str) -> list[str]:
        issues = []
        if memo.count("[") < 2:
            issues.append("Fewer than 2 cited documents; consider a broader search.")
        if "?" in memo:
            issues.append("Memo contains a question mark; verify completeness.")
        return issues

    def research(self, query: str) -> dict:
        docs = self.vault.search(query)
        memo = self._draft_memo(query, docs)
        return {"query": query, "refinement": self.suggest_prompt_refinement(query),
                "memo": memo, "review_issues": self._self_review(memo)}


def build_demo_vault() -> Vault:
    vault = Vault()
    for title, text in [
        ("Force Majeure Clause Guide",
         "A force majeure clause excuses performance when extraordinary events beyond a party's control occur."),
        ("Frustration of Purpose Doctrine",
         "Courts apply frustration when a contract's core purpose is destroyed by supervening events."),
        ("UCC Section 2-615",
         "UCC 2-615 excuses sellers when performance becomes impracticable due to unforeseen contingencies."),
    ]:
        vault.add(title, text)
    return vault


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="force majeure clause")
    args = parser.parse_args()
    agent = ProtegeAgent(build_demo_vault())
    result = agent.research(args.query)
    print("Refinement suggestion:", result["refinement"], "\n\n" + result["memo"])
    print("\nSelf-review:", result["review_issues"] or ["None -- memo looks solid."])


if __name__ == "__main__":
    main()
