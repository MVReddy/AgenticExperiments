"""LangGraph-style stateful workflow (inspired by LangGraph, ~40k GitHub stars).

Simulates: a graph of nodes (intake -> research -> draft -> review) passing
a shared State object, with checkpoint comments marking where persistence
and human-in-the-loop would hook in.

Run:
    python experiments/08_langgraph_style_graph.py --matter "trademark dispute"

CHALLENGE: Add a conditional edge that loops draft -> research when review fails.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field


@dataclass
class State:
    matter: str
    facts: list[str] = field(default_factory=list)
    authorities: list[str] = field(default_factory=list)
    memo: str = ""
    review_notes: list[str] = field(default_factory=list)
    # CHECKPOINT: in LangGraph this state would be persisted via a
    # checkpointer (e.g. SqliteSaver) so the run can resume after interruption.


def node_intake(state: State) -> State:
    state.facts.append(f"Client matter opened: {state.matter}")
    return state


def node_research(state: State) -> State:
    state.authorities.append("15 U.S.C. \u00a7 1114 (trademark infringement)")
    state.authorities.append("Polaroid factors for likelihood of confusion")
    return state


def node_draft(state: State) -> State:
    state.memo = (
        f"MEMO -- {state.matter}\n"
        f"Facts: {'; '.join(state.facts)}\n"
        f"Authorities: {'; '.join(state.authorities)}"
    )
    return state


def node_review(state: State) -> State:
    if len(state.authorities) < 2:
        state.review_notes.append("Add more authority.")
    else:
        state.review_notes.append("Approved -- citations look complete.")
    return state


def run_graph(matter: str) -> State:
    state = State(matter=matter)
    for node in (node_intake, node_research, node_draft, node_review):
        # CHECKPOINT: save state here; HUMAN-IN-THE-LOOP could pause before review.
        state = node(state)
    return state


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matter", default="trademark dispute")
    args = parser.parse_args()
    final = run_graph(args.matter)
    print(final.memo)
    print("\nReview:", final.review_notes)


if __name__ == "__main__":
    main()
