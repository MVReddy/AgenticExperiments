"""CoCounsel-style deep research + verification (inspired by Thomson Reuters CoCounsel).

Simulates: an agent that writes a research memo, then runs a verification
pass over its citations, flagging hallucinated authorities not found in the
corpus — plus a tabular question-x-document analysis view.

Run:
    python experiments/02_cocounsel_style_deep_research.py

CHALLENGE: Extend verify_citations() to also check pin-cite page numbers.
"""
from __future__ import annotations

import re

CORPUS = {
    "Miranda v. Arizona, 384 U.S. 436 (1966)": "custodial interrogation warnings",
    "Terry v. Ohio, 392 U.S. 1 (1968)": "stop and frisk reasonable suspicion",
    "Gideon v. Wainwright, 372 U.S. 335 (1963)": "right to counsel for felonies",
}

MEMO_DRAFT = """MEMO -- Custodial Interrogation

Under Miranda v. Arizona, 384 U.S. 436 (1966), suspects in custody must be
warned before interrogation. See also Fake v. Nobody, 999 F. Supp. 1 (2099),
which supposedly extends Miranda to emails. Terry v. Ohio, 392 U.S. 1 (1968)
is inapposite (stop-and-frisk, not interrogation)."""

CITE_RE = re.compile(
    r"[A-Z][A-Za-z.'&()\-]*[ \t]+v\.[ \t]+[A-Z][A-Za-z.'&()\-]*"
    r"[ \t]*,[ \t]*\d+[ \t]+[\w. ]+?\d+[ \t]*\(\d{4}\)"
)


class DeepResearchAgent:
    def research_memo(self, topic: str) -> str:
        return f"# Deep Research: {topic}\n\n{MEMO_DRAFT}"

    def verify_citations(self, memo: str) -> list[dict]:
        """Flag citations not present in the verified corpus."""
        results = []
        for cite in CITE_RE.findall(memo):
            cite = " ".join(cite.split())
            parties = cite.split(",")[0].strip().lower()
            known = any(k.split(",")[0].strip().lower() in parties
                        or k.split(",")[0].strip().lower() in cite.lower()
                        for k in CORPUS)
            results.append({
                "citation": cite,
                "verified": known,
                "note": "OK" if known else "HALLUCINATED -- not in corpus",
            })
        return results

    def tabular_analysis(self, docs: list[str], questions: list[str]) -> None:
        """Print a question x document grid."""
        header = ["Question \\ Doc"] + [f"D{i + 1}" for i in range(len(docs))]
        rows = [header]
        for q in questions:
            row = [q]
            for d in docs:
                hit = "YES" if any(w in d.lower() for w in q.lower().split()[:2]) else "--"
                row.append(hit)
            rows.append(row)
        widths = [max(len(str(r[i])) for r in rows) + 2 for i in range(len(header))]
        for r in rows:
            print("".join(str(c).ljust(w) for c, w in zip(r, widths)))
        print()


def main() -> None:
    agent = DeepResearchAgent()
    memo = agent.research_memo("custodial interrogation")
    print(memo)
    print("\n--- Citation verification ---")
    for v in agent.verify_citations(memo):
        tag = "OK  " if v["verified"] else "FLAG"
        print(f"[{tag}] {v['citation']} -- {v['note']}")
    print("\n--- Tabular analysis ---")
    agent.tabular_analysis(
        docs=["Miranda warnings required in custody",
              "Terry stops need reasonable suspicion"],
        questions=["warnings required", "reasonable suspicion", "email privacy"],
    )


if __name__ == "__main__":
    main()
