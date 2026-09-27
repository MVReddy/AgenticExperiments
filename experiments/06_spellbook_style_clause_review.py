"""Spellbook-style contract review (inspired by Spellbook AI).

Simulates: scanning contract text for risky patterns and benchmarking
each finding against market-standard language.

Run:
    python experiments/06_spellbook_style_clause_review.py

CHALLENGE: Add a --fix flag that suggests replacement language for each risk.
"""
from __future__ import annotations

RISKY_PATTERNS: list[tuple[str, str, str]] = [
    ("unlimited liability", "HIGH",
     "Market standard caps liability at 12 months' fees."),
    ("perpetual", "MEDIUM",
     "Market standard limits term to 1-3 years with renewal."),
    ("sole discretion", "MEDIUM",
     "Market standard requires 'reasonable discretion'."),
    ("waive", "HIGH",
     "Waivers of jury trial / class action are often unenforceable."),
    ("indemnify", "LOW",
     "Mutual indemnification is market standard."),
]

SAMPLE_CONTRACT = """This Agreement shall be perpetual. Licensee accepts
unlimited liability for all claims. Licensor may terminate at its sole
discretion. Licensee hereby waive any right to jury trial. Each party
shall indemnify the other for third-party claims."""


def review(text: str) -> list[dict]:
    findings = []
    normalized = " ".join(text.lower().split())
    for pattern, severity, benchmark in RISKY_PATTERNS:
        if pattern in normalized:
            sentence = next(
                (s.strip() for s in normalized.split(".") if pattern in s), "")
            findings.append({
                "pattern": pattern,
                "severity": severity,
                "context": sentence,
                "benchmark": benchmark,
            })
    return findings


def main() -> None:
    findings = review(SAMPLE_CONTRACT)
    print(f"Reviewed contract -- {len(findings)} risk(s) found.\n")
    for f in findings:
        print(f"[{f['severity']}] '{f['pattern']}'")
        print(f"  Context:   {f['context']}")
        print(f"  Benchmark: {f['benchmark']}\n")


if __name__ == "__main__":
    main()
