"""CrewAI-style multi-agent crew (inspired by CrewAI, ~57k GitHub stars).

Simulates: a sequential crew -- Researcher -> Drafter -> Reviewer -- where
each agent has a role, goal, and backstory, and task outputs flow down
the chain as context.

Run:
    python experiments/07_crewai_style_crew.py --topic "data breach notification"

CHALLENGE: Add a parallel 'Critic' agent whose feedback loops back to the Drafter.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass
class Agent:
    role: str
    goal: str
    backstory: str

    def run(self, task: str, context: str = "") -> str:
        prefix = {"Researcher": "FINDINGS", "Drafter": "DRAFT",
                  "Reviewer": "REVIEW"}.get(self.role, "OUTPUT")
        snippet = context[:80].replace("\n", " ")
        return f"[{prefix} by {self.role}] Task: {task} | Context: {snippet}..."


@dataclass
class Task:
    description: str
    agent: Agent


class Crew:
    def __init__(self, agents: list[Agent], tasks: list[Task]) -> None:
        self.agents = agents
        self.tasks = tasks

    def kickoff(self) -> dict[str, str]:
        outputs: dict[str, str] = {}
        context = ""
        for task in self.tasks:
            out = task.agent.run(task.description, context)
            outputs[task.agent.role] = out
            context = out  # downstream agents see upstream output
        return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="data breach notification laws")
    args = parser.parse_args()

    researcher = Agent("Researcher", "Find key authorities",
                       "A meticulous paralegal who never misses a footnote.")
    drafter = Agent("Drafter", "Write the client memo",
                    "A senior associate with a plain-English style.")
    reviewer = Agent("Reviewer", "Check accuracy and tone",
                     "A partner who red-pens everything twice.")

    crew = Crew(
        agents=[researcher, drafter, reviewer],
        tasks=[
            Task(f"Research {args.topic}", researcher),
            Task("Draft client memo from findings", drafter),
            Task("Review memo for errors", reviewer),
        ],
    )
    for role, output in crew.kickoff().items():
        print(f"{role}:\n  {output}\n")


if __name__ == "__main__":
    main()
