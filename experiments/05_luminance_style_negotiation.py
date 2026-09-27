"""Luminance-style autonomous negotiation (inspired by Luminance Autopilot).

Simulates: two agents (Company vs Counterparty) negotiating NDA clause
positions over rounds, each conceding toward the other until they agree
or hit max_rounds.

Run:
    python experiments/05_luminance_style_negotiation.py --max-rounds 6

CHALLENGE: Add a third clause (liability cap) and a walk-away threshold.
"""
from __future__ import annotations

import argparse

CLAUSES = ["confidentiality_years", "non_solicit_months"]


class NDAAgent:
    """Negotiates NDA clause positions toward the middle."""

    def __init__(self, name: str, positions: dict[str, int],
                 flexibility: float = 0.5) -> None:
        self.name = name
        self.positions = dict(positions)
        self.flexibility = flexibility

    def offer(self, clause: str, counterpart_offer: int) -> int:
        mine = self.positions[clause]
        move = int((counterpart_offer - mine) * self.flexibility)
        self.positions[clause] = mine + move
        return self.positions[clause]


def negotiate(a: NDAAgent, b: NDAAgent, max_rounds: int = 6) -> dict:
    history: list[tuple[int, dict]] = []
    for rnd in range(1, max_rounds + 1):
        round_offers = {}
        for clause in CLAUSES:
            a_offer = a.offer(clause, b.positions[clause])
            b_offer = b.offer(clause, a.positions[clause])
            round_offers[clause] = (a_offer, b_offer)
        history.append((rnd, dict(round_offers)))
        if all(abs(x - y) <= 1 for x, y in round_offers.values()):
            return {"agreed": True, "rounds": rnd,
                    "final": round_offers, "history": history}
    return {"agreed": False, "rounds": max_rounds,
            "final": history[-1][1], "history": history}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rounds", type=int, default=6)
    args = parser.parse_args()

    company = NDAAgent("Company",
                       {"confidentiality_years": 5, "non_solicit_months": 24})
    counter = NDAAgent("Counterparty",
                       {"confidentiality_years": 1, "non_solicit_months": 6})
    result = negotiate(company, counter, args.max_rounds)
    for rnd, offers in result["history"]:
        print(f"Round {rnd}: {offers}")
    status = "AGREED" if result["agreed"] else "NO DEAL -- escalate to human"
    print(f"\n{status} after {result['rounds']} round(s).")


if __name__ == "__main__":
    main()
