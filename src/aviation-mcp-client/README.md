# Aviation MCP Client

LangChain-based CLI client for the Aviation MCP server. Two modes: interactive REPL (natural language queries via LLM agent) and batch testing (direct MCP tool calls, no LLM required).

## Modes

### Batch Test Mode (`--test`)

Connects directly to the MCP server via SSE and runs 8 predefined test scenarios. No LLM API key needed.

```bash
uv run python -m src.client --test --mcp-url http://localhost:8000/sse
```

```
Connecting to MCP server at http://localhost:8000/sse...

  [PASS] Flight lookup at BDL
  [PASS] Flight by number
  [PASS] Unknown airport returns empty
  [PASS] Gates at JFK
  [PASS] Specific gate
  [PASS] Unknown gate returns empty
  [PASS] Weather at LAX
  [PASS] Unknown airport weather

Results: 8/8 passed
```

Exit code 0 = all pass, 1 = any fail.

### Interactive REPL Mode (default)

Connects to the MCP server and creates a LangChain ReAct agent with the available tools. Requires an LLM.

**Anthropic** (default):
```bash
LLM_API_KEY=your-key uv run python -m src.client --mcp-url http://localhost:8000/sse
```

**OpenAI**:
```bash
LLM_PROVIDER=openai LLM_MODEL=gpt-4o LLM_API_KEY=your-key \
  uv run python -m src.client --mcp-url http://localhost:8000/sse
```

**Ollama** (local, no API key):
```bash
LLM_PROVIDER=ollama LLM_MODEL=llama3.2 \
  uv run python -m src.client --mcp-url http://localhost:8000/sse
```

```
Aviation MCP Client (type 'quit' to exit)
Connected to MCP server at http://localhost:8000/sse
Tools available: ['get_flight_status', 'get_gate_info', 'get_weather']

> What flights are at BDL?
> What's the weather like at JFK?
> quit
Goodbye!
```

## Project Structure

```
src/aviation-mcp-client/
├── pyproject.toml
├── src/
│   ├── client.py          # Entry point: argparse, mode dispatch
│   ├── config.py          # Config dataclass with env var loading
│   ├── agent.py           # LangChain agent setup (MultiServerMCPClient + ReAct)
│   └── test_runner.py     # Batch test scenarios and runner
└── tests/
    └── test_client.py     # 21 unit tests
```

## Setup

```bash
uv sync
```

## CLI Arguments

```
python -m src.client [--test] [--mcp-url URL]

  --test       Run batch tests instead of interactive REPL
  --mcp-url    Override MCP server SSE URL (default: http://localhost:8000/sse)
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_SERVER_URL` | `http://localhost:8000/sse` | MCP server SSE endpoint |
| `LLM_PROVIDER` | `anthropic` | LLM provider (`anthropic`, `openai`, or `ollama`) |
| `LLM_MODEL` | `claude-sonnet-4-5-20250929` | Model name |
| `LLM_API_KEY` | (none) | API key (not needed for Ollama) |
| `LLM_BASE_URL` | (none) | Custom API base URL (Ollama default: `http://localhost:11434/v1`) |

CLI `--mcp-url` overrides the `MCP_SERVER_URL` environment variable.

## Testing

```bash
uv run pytest tests/ -v
```

21 tests covering:
- **Config** (8 tests): Defaults, env var overrides, Anthropic/OpenAI/Ollama model creation, custom base URL
- **TestScenario** (3 tests): Dataclass creation, tool coverage, scenario count
- **check_result** (6 tests): Non-empty/empty validation, invalid JSON, dict responses
- **run_batch_tests** (2 tests): All-pass scenario, failure detection (with mocked MCP session)

All tests use mocks — no running MCP server or LLM API key required.

## Test Scenarios

The batch runner exercises all 3 MCP tools with positive and negative cases:

| Scenario | Tool | Params | Expected |
|----------|------|--------|----------|
| Flight lookup at BDL | `get_flight_status` | airport=BDL | Non-empty |
| Flight by number | `get_flight_status` | airport=BDL, flight_number=DL1234 | Non-empty |
| Unknown airport | `get_flight_status` | airport=XXX | Empty |
| Gates at JFK | `get_gate_info` | airport=JFK | Non-empty |
| Specific gate | `get_gate_info` | airport=BDL, gate_number=A1 | Non-empty |
| Unknown gate | `get_gate_info` | airport=JFK, gate_number=Z99 | Empty |
| Weather at LAX | `get_weather` | airport=LAX | Non-empty |
| Unknown airport weather | `get_weather` | airport=XXX | Empty |

## Dependencies

- `langchain>=0.3.0` -- Agent orchestration framework
- `langgraph>=0.2.0` -- ReAct agent implementation
- `langchain-mcp-adapters>=0.1.0` -- MCP SSE client adapter
- `langchain-anthropic>=0.3.0` -- Claude LLM integration
- `langchain-openai>=0.3.0` -- OpenAI and Ollama (via OpenAI-compatible API) integration
- `mcp>=1.25,<2` -- MCP protocol client (used by batch mode)

## Design Decisions

- **Batch mode bypasses the LLM entirely**, calling MCP tools directly via `mcp.client.sse.sse_client` and `ClientSession`. This makes automated testing fast, deterministic, and free of API key requirements.
- **Interactive mode uses `MultiServerMCPClient`** as an async context manager. The REPL loop runs inside the context because the agent and tools are only valid within it.
- **The client is not Dockerized** — it runs on the host machine connecting to `localhost:8000`. This keeps the testing workflow simple.
