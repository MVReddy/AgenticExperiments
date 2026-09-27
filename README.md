# AgenticExperiments

Daily hands-on experiments in agentic AI for legal work — inspired by the new
wave of legal AI products and the open-source agent frameworks behind them.

## Inspiration

**Legal AI products**

| Product | What we borrow for these experiments |
|---|---|
| LexisNexis Protégé | Multi-step agentic tasks, private Vault, prompt refinement, self-review |
| Thomson Reuters CoCounsel | Deep Research memos + citation verification |
| Harvey | Q&A with confidence scores and cited sources |
| Legora | Tabular / grid review across many documents |
| Spellbook | Clause-level risk review with market benchmarks |
| Luminance Autopilot | Autonomous negotiation over rounds |

**Open-source agent frameworks**

| Framework | Stars (approx.) | Experiment |
|---|---|---|
| CrewAI | ~57k | 07 — role-based agent crew |
| LangGraph | ~40k | 08 — stateful node graph |
| smolagents | ~28k | 09 — code-executing tool agent |
| OpenAI Agents SDK | ~29k | patterns used across 01–03 |
| Google ADK | ~21k | patterns used across 01–03 |
| PydanticAI | ~19k | typed-agent patterns in 03, 07 |

## Quick start

```bash
pip install -r requirements.txt
python experiments/01_protege_style_research_agent.py --query "force majeure"
```

Everything runs on the Python standard library — **no API keys needed**.

## Daily play

1. Run `python experiments/10_daily_challenge.py` to get today's 3 challenges
   (deterministic per date — everyone gets the same set).
2. Pick one challenge and hack on the matching experiment file.
3. Commit your solution and share what you learned.

## Experiments

| # | File | Simulates |
|---|---|---|
| 01 | `01_protege_style_research_agent.py` | Protégé-style research: Vault, prompt refinement, draft memo, self-review |
| 02 | `02_cocounsel_style_deep_research.py` | CoCounsel-style deep research, citation verification, tabular analysis |
| 03 | `03_harvey_style_qa.py` | Harvey-style Q&A with confidence scores and source citations |
| 04 | `04_legora_style_grid_review.py` | Legora-style grid review: prompts × documents |
| 05 | `05_luminance_style_negotiation.py` | Luminance-style autonomous NDA negotiation over rounds |
| 06 | `06_spellbook_style_clause_review.py` | Spellbook-style clause risk review with market benchmarks |
| 07 | `07_crewai_style_crew.py` | CrewAI-style crew: Researcher → Drafter → Reviewer |
| 08 | `08_langgraph_style_graph.py` | LangGraph-style stateful workflow with checkpoints |
| 09 | `09_smolagents_style_tool_agent.py` | smolagents-style code agent with sandboxed tools |
| 10 | `10_daily_challenge.py` | Daily challenge picker (3 of 12, seeded by date) |

## Contributing

Each experiment file ends with a `CHALLENGE:` line in its docstring — that's
your next exercise. Keep solutions small, stdlib-only, and fun.
