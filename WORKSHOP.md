# 50-Minute Workshop Runbook

## 0–5 — What is an Agent?
LLM → Tool Calling → Agent Loop → MCP

Key phrase:
> LLM gives intelligence. Tools give capabilities. The agent connects them through a loop.

## 5–10 — Architecture
User → Agent/LLM → Tools → Results → Agent → Final Answer

## 10–15 — Local LLM
Run:
```bash
python 01_llm/main.py
```

## 15–22 — Tool Calling
Run:
```bash
python 02_tools/main.py
```
Ask: What changed? The model selected a tool.

## 22–30 — Agent Loop
Run:
```bash
python 03_agent/main.py
```
Focus on the visible loop:
1. Ask model
2. Detect tool call
3. Execute tool
4. Send result back
5. Ask model again

## 30–36 — Final Research Agent
Run:
```bash
python 05_final/agent.py
```
Point out the visible tool calls.

## 36–42 — MCP
Run:
```bash
mcp dev 04_mcp/server.py
```
Explain that MCP standardizes how AI applications discover and use tools.

## 42–46 — Inspector
Manually call `calculate`, then show the other tools.

## 46–48 — Production Reality
Mention permissions, sandboxing, retries, timeouts, observability, prompt injection, privacy and human approval.

## 48–50 — Student Challenge
Ask students to design one new tool:
- PDF reader
- GitHub search
- course schedule
- SQL query
- CSV analyzer

## Emergency fallback
If Ollama/model fails:
1. Run the MCP Inspector demo.
2. Run `02_tools/main.py`.
3. Explain the loop from `03_agent/main.py`.
4. Show the final architecture and let students modify a tool.
