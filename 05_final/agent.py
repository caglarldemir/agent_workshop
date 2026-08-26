import json
import re
from pathlib import Path
from ollama import chat

MODEL = "qwen3:4b"
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

def calculate(a: float, b: float, operation: str) -> float:
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b
    raise ValueError(f"Unsupported operation: {operation}")

def search_web(query: str) -> str:
    """Offline demo search tool."""
    snippets = {
        "python": "Python has a large AI/ML ecosystem including PyTorch, scikit-learn and many LLM libraries.",
        "go": "Go is known for simple deployment, concurrency and strong performance in backend/cloud services.",
        "java": "Java has a mature enterprise ecosystem, strong tooling and widely deployed backend infrastructure.",
        "ai agents": "AI agents combine an LLM with tools and an execution loop that lets the system take actions based on model decisions.",
    }
    q = query.lower()
    matches = [v for k, v in snippets.items() if k in q]
    return "\n".join(f"- {x}" for x in matches) or (
        "No live web search is configured. Try Python, Go, Java, or AI agents."
    )

def save_report(title: str, content: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "-", title).strip("-").lower()
    path = REPORT_DIR / f"{safe or 'report'}.md"
    path.write_text(f"# {title}\n\n{content}\n", encoding="utf-8")
    return f"Saved report to {path}"

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the available research index. Use this before factual comparisons.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a basic arithmetic calculation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                    },
                },
                "required": ["a", "b", "operation"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_report",
            "description": "Save a Markdown research report locally.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["title", "content"],
            },
        },
    },
]

TOOL_MAP = {
    "search_web": search_web,
    "calculate": calculate,
    "save_report": save_report,
}

def run_agent(question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a research agent. Break complex requests into steps. "
                "Search before factual claims. Use tools when useful. "
                "You may save a final Markdown report."
            ),
        },
        {"role": "user", "content": question},
    ]

    for step in range(10):
        response = chat(model=MODEL, messages=messages, tools=TOOL_DEFINITIONS)

        if not response.message.tool_calls:
            return response.message.content

        messages.append(response.message)

        for call in response.message.tool_calls:
            name = call.function.name
            args = call.function.arguments
            print(f"\n[step {step + 1}] TOOL: {name}")
            print(f"           ARGS: {args}")

            if name not in TOOL_MAP:
                raise ValueError(f"Unknown tool: {name}")

            result = TOOL_MAP[name](**args)
            print(f"           RESULT: {result}")

            messages.append({
                "role": "tool",
                "tool_name": name,
                "content": json.dumps(result),
            })

    raise RuntimeError("Agent stopped after too many tool steps.")

if __name__ == "__main__":
    print("=" * 70)
    print("BUILD YOUR OWN AI AGENT — FINAL DEMO")
    print("=" * 70)

    question = (
        "Compare Python, Java and Go for AI engineering in 2026. "
        "Research the topic and give me a recommendation. "
        "Save a short report if useful."
    )

    answer = run_agent(question)

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)
    print(answer)
