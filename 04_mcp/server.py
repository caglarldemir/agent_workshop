from mcp.server import MCPServer

mcp = MCPServer("Research Workshop Tools")

@mcp.tool()
def calculate(a: float, b: float, operation: str) -> float:
    """Perform a basic arithmetic calculation."""
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

@mcp.tool()
def search_web(query: str) -> str:
    """Return deterministic offline research snippets for the workshop."""
    snippets = {
        "python": "Python has a large AI/ML ecosystem including PyTorch, scikit-learn and many LLM libraries.",
        "go": "Go is known for simple deployment, concurrency and strong performance in backend/cloud services.",
        "java": "Java has a mature enterprise ecosystem, strong tooling and widely deployed backend infrastructure.",
        "ai agents": "AI agents combine an LLM with tools and an execution loop that lets the system take actions based on model decisions.",
    }
    q = query.lower()
    matches = [text for key, text in snippets.items() if key in q]
    return "\n".join(f"- {x}" for x in matches) or (
        "No live web search is configured. Try Python, Go, Java, or AI agents."
    )

@mcp.tool()
def save_report(title: str, content: str) -> str:
    """Save a Markdown report locally."""
    from pathlib import Path
    import re
    reports = Path("reports")
    reports.mkdir(exist_ok=True)
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "-", title).strip("-").lower()
    path = reports / f"{safe or 'report'}.md"
    path.write_text(f"# {title}\n\n{content}\n", encoding="utf-8")
    return f"Saved report to {path}"

if __name__ == "__main__":
    mcp.run()
