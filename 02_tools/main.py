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

tools = [{
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

messages = [{
    "role": "user",
    "content": "What is 1245 multiplied by 37?"
}]

response = chat(model=MODEL, messages=messages, tools=tools)

if response.message.tool_calls:
    for call in response.message.tool_calls:
        args = call.function.arguments
        result = calculate(**args)
        print(f"Tool selected: {call.function.name}")
        print(f"Tool arguments: {args}")
        print(f"Tool result: {result}")
else:
    print(response.message.content)
