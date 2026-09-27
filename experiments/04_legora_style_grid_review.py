"""Legora-style tabular review (inspired by Legora's AI grid review).

Simulates: running the same review prompt across many documents and
rendering the answers in a grid — like reviewing a data room of contracts.

Run:
    python experiments/04_legora_style_grid_review.py

CHALLENGE: Add CSV export of the grid behind a --csv flag.
"""
from __future__ import annotations

DOCS = {
    "MSA_Acme.pdf": "This agreement has a 30-day termination for convenience "
                    "clause and mutual indemnification.",
    "MSA_Beta.pdf": "Termination requires 90 days notice. Indemnification "
                    "is one-way in favor of Beta.",
    "NDA_Gamma.pdf": "Mutual NDA with 2-year confidentiality period and "
                     "no termination clause.",
}

PROMPTS = [
    "termination notice period",
    "indemnification",
    "confidentiality period",
]

KEYWORDS = {
    "termination notice period": ["30-day", "90 days", "termination"],
    "indemnification": ["indemnification", "indemnify"],
    "confidentiality period": ["confidentiality", "2-year"],
}


def run_cell(doc_text: str, prompt: str) -> str:
    """Simulated LLM cell: keyword-overlap answer extraction."""
    text = doc_text.lower()
    hits = [k for k in KEYWORDS.get(prompt, []) if k in text]
    if not hits:
        return "Not found"
    for sent in doc_text.split("."):
        if hits[0] in sent.lower():
            return sent.strip()
    return ", ".join(hits)


def print_grid(docs: dict[str, str], prompts: list[str]) -> None:
    names = list(docs)
    rows = [["Prompt \\ Document"] + names]
    for p in prompts:
        rows.append([p] + [run_cell(docs[n], p) for n in names])
    widths = [max(len(str(r[i])) for r in rows) + 3 for i in range(len(names) + 1)]
    for ri, r in enumerate(rows):
        print("".join(str(c).ljust(w) for c, w in zip(r, widths)))
        if ri == 0:
            print("-" * sum(widths))


def main() -> None:
    print_grid(DOCS, PROMPTS)


if __name__ == "__main__":
    main()
