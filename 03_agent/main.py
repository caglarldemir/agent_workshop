import json
from ollama import chat

MODEL = "qwen3:4b"

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

TOOLS = [{
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
                    "enum": ["add", "subtract", "multiply", "divide"]
                },
            },
            "required": ["a", "b", "operation"],
        },
    },
}]

TOOL_MAP = {"calculate": calculate}

def run_agent(user_question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Use tools when useful. "
                "After receiving a tool result, answer clearly."
            ),
        },
        {"role": "user", "content": user_question},
    ]

    for step in range(6):
        response = chat(model=MODEL, messages=messages, tools=TOOLS)

        if not response.message.tool_calls:
            return response.message.content

        messages.append(response.message)

        for call in response.message.tool_calls:
            name = call.function.name
            args = call.function.arguments
            print(f"[agent] calling {name}({args})")

            if name not in TOOL_MAP:
                raise ValueError(f"Unknown tool: {name}")

            result = TOOL_MAP[name](**args)
            messages.append({
                "role": "tool",
                "tool_name": name,
                "content": json.dumps(result),
            })

    raise RuntimeError("Agent stopped after too many tool steps.")

if __name__ == "__main__":
    print(run_agent("What is 1245 multiplied by 37?"))
