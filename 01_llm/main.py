from ollama import chat

MODEL = "qwen3:4b"

response = chat(
    model=MODEL,
    messages=[{
        "role": "user",
        "content": "Explain AI agents in exactly three simple sentences."
    }],
)

print(response.message.content)
