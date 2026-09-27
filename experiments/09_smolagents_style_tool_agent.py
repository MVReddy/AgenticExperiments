"""smolagents-style code agent (inspired by HuggingFace smolagents, ~28k stars).

Simulates: an agent that writes Python code calling sandboxed tools, then
executes it via exec() in a limited namespace (tools only, no builtins).

Run:
    python experiments/09_smolagents_style_tool_agent.py

CHALLENGE: Add a third tool (e.g. check_deadline) and a task that needs all three.
"""
from __future__ import annotations

STATUTES = {
    "limitations": "Personal injury actions must be filed within 2 years.",
    "contract": "Written contract claims: 4-year limitations period.",
}


def search_statute(topic: str) -> str:
    """Simulated tool: look up a statute by topic."""
    return STATUTES.get(topic, "No statute found.")


def summarize(text: str) -> str:
    """Simulated tool: summarize text."""
    return text[:60].rstrip() + ("..." if len(text) > 60 else "")


agent_code = '''
result = search_statute("limitations")
brief = summarize(result)
final_answer = f"Statute: {result} | Brief: {brief}"
'''


def run_agent(code: str) -> dict:
    namespace = {"search_statute": search_statute, "summarize": summarize}
    # Limited namespace: tools only, no builtins -- the agent can only
    # call what we explicitly hand it, like smolagents' sandbox.
    exec(compile(code, "<agent>", "exec"), {"__builtins__": {}}, namespace)
    return {"final_answer": namespace.get("final_answer", "No answer produced.")}


def main() -> None:
    print("Agent code:\n" + agent_code)
    result = run_agent(agent_code)
    print("Result:", result["final_answer"])


if __name__ == "__main__":
    main()
