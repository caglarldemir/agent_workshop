# Build Your Own AI Agent — Research Agent Workshop

A 50-minute university workshop building an AI agent step-by-step with a local open-source model, Python tools, an explicit agent loop, and MCP.

## Stack
- Python 3.10+
- Ollama
- Qwen3 (`qwen3:4b`)
- Official MCP Python SDK v2
- No paid API required

## Journey
1. `01_llm/` — call a local LLM
2. `02_tools/` — define a tool and let the model select it
3. `03_agent/` — implement the tool execution loop
4. `04_mcp/` — expose tools through MCP
5. `05_final/` — final Research Agent

## Setup

Install Python 3.10+ and Ollama, then:

```bash
ollama pull qwen3:4b
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell:
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Run checkpoints from the repository root:

```bash
python 01_llm/main.py
python 02_tools/main.py
python 03_agent/main.py
python 05_final/agent.py
```

MCP Inspector:

```bash
mcp dev 04_mcp/server.py
```

## Demo prompts
- `What is 1245 multiplied by 37?`
- `Compare Python, Java and Go for AI engineering in 2026.`
- `Research AI agents and save a short report.`

The search tool is intentionally offline/deterministic so the workshop does not require a paid web-search API. Replace it later with a real search provider.

## Teaching principle

The agent loop is deliberately written without LangChain/LangGraph so students can see the mechanism:

**LLM + tools + execution loop = minimal agent**

MCP is introduced afterward as a standard interface for exposing tools.

## Safety

The calculator does not use `eval()`.
