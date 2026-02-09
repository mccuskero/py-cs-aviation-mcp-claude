# PRP: Phase 3 — CLI Test Client & Docker Compose Orchestration

## Discovery Summary

### Initial Task Analysis

Build a LangChain-based CLI test client that connects to the MCP server (Phase 2) and exercises all three aviation tools. Additionally, create the `docker-compose.yml` that orchestrates all four services (3 C# microservices + Python MCP server) plus the CLI client. This phase ties the entire architecture together and provides the end-to-end integration test.

### User Clarifications Received

- **Question**: Interactive or batch CLI client?
- **Answer**: Both — interactive REPL for demos + `--test` flag for batch validation
- **Impact**: Two modes implemented: interactive agent loop and automated test runner

- **Question**: CLI client framework?
- **Answer**: LangChain v1.2.6+ with langchain-mcp-adapters
- **Impact**: Uses `MultiServerMCPClient` or SSE client adapter to connect to MCP server

### Missing Requirements Identified

- LLM provider for LangChain agent (needed for interactive mode — can use any LangChain-supported model)
- Test scenarios for batch mode (defined below)
- docker-compose networking and health check configuration

## Goal

Create a LangChain CLI client with two modes (interactive REPL and batch test runner) that connects to the MCP server via SSE and exercises all three aviation tools. Create `docker-compose.yml` to orchestrate the full stack. Validate the end-to-end architecture: CLI → MCP Server → C# Microservices → JSON stubs and back.

## Why

- Completes the architectural demonstration — shows the full request lifecycle
- Interactive mode lets users experience the MCP pattern hands-on
- Batch mode provides automated integration validation (CI-friendly)
- docker-compose makes the entire demo one command: `docker-compose up`
- Proves the cross-language, cross-service architecture works end-to-end

## What

### User-visible Behavior

**Interactive mode** (`python client.py`):
- Connects to MCP server via SSE
- Presents a REPL prompt
- User types natural language queries (e.g., "What flights are at BDL?")
- LangChain agent routes to appropriate MCP tool, displays results
- Type `quit` or `exit` to stop

**Batch mode** (`python client.py --test`):
- Connects to MCP server via SSE
- Runs predefined test scenarios against all three tools
- Reports pass/fail for each scenario
- Exits with code 0 (all pass) or 1 (any fail)

**docker-compose**:
- `docker-compose up --build` starts everything
- All services reachable on their assigned ports
- Health checks ensure C# services are ready before MCP server starts

### Success Criteria

- [ ] CLI client connects to MCP server via SSE
- [ ] Interactive REPL: user queries routed to correct MCP tools, results displayed
- [ ] Batch mode: all predefined test scenarios pass
- [ ] docker-compose.yml starts all 4 services with correct networking
- [ ] Health checks ensure startup ordering (C# services → MCP server)
- [ ] Full end-to-end test: CLI → MCP → C# → JSON data → response displayed
- [ ] Debug mode on MCP server shows protocol trace during client interaction
- [ ] pytest tests pass for client module

## All Needed Context

### Research Phase Summary

- **Codebase patterns found**: Phase 1 (C# services) and Phase 2 (MCP server) provide all upstream dependencies
- **External research needed**: Yes — langchain-mcp-adapters SSE client, LangGraph create_react_agent
- **Knowledge gaps identified**: LangChain + MCP SSE integration specifics

**Key research findings:**

1. **langchain-mcp-adapters** is the official LangChain ↔ MCP bridge package
2. **MultiServerMCPClient** connects to MCP servers (supports SSE transport)
3. **create_react_agent** from LangGraph creates agents that use MCP tools
4. Pattern: `async with MultiServerMCPClient(config) as client:` → `client.get_tools()` → `create_react_agent(model, tools)`
5. SSE client: `from mcp.client.sse import sse_client` for low-level access
6. Known issue: SSE transport deprecated; `langchain-mcp-adapters` may shift to Streamable HTTP
7. Tool invocation is async: use `await agent.ainvoke({"messages": "query"})`

### Documentation & References

```yaml
- url: https://github.com/langchain-ai/langchain-mcp-adapters
  why: Official LangChain MCP adapter — SSE client, tool loading, agent creation

- url: https://python.langchain.com/api_reference/langchain/agents/langchain.agents.react.agent.create_react_agent.html
  why: ReAct agent creation for tool-calling

- url: https://docs.docker.com/compose/compose-file/
  why: docker-compose.yml syntax, depends_on, healthcheck, networks

- url: https://github.com/modelcontextprotocol/python-sdk
  why: MCP client SSE connection patterns

- file: docs/prps/phase1-csharp-microservices.md
  why: C# service ports (5001, 5002, 5003), API contracts

- file: docs/prps/phase2-python-mcp-server.md
  why: MCP server SSE endpoint (port 8000), tool names, debug mode

- file: CLAUDE.md
  why: Project conventions, architecture overview
```

### Current Codebase Tree (after Phase 1 + Phase 2)

```
py-cs-aviation-mcp-claude/
├── src/
│   ├── aviation-mcp/       # Phase 2: Python MCP server on port 8000
│   ├── flight-status/      # Phase 1: C# service on port 5001
│   ├── gate-info/          # Phase 1: C# service on port 5002
│   └── weather/            # Phase 1: C# service on port 5003
```

### Desired Codebase Tree (Phase 3 additions)

```
py-cs-aviation-mcp-claude/
├── docker-compose.yml                  # Orchestrates all services
├── src/
│   ├── aviation-mcp-client/
│   │   ├── pyproject.toml              # uv project config
│   │   └── src/
│   │       ├── __init__.py
│   │       ├── client.py               # Main entry point (REPL + batch modes)
│   │       ├── agent.py                # LangChain agent setup
│   │       ├── test_runner.py          # Batch test scenarios
│   │       └── config.py              # MCP server URL, LLM config
│   │   └── tests/
│   │       ├── __init__.py
│   │       └── test_client.py
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: langchain-mcp-adapters requires specific version compatibility
# Pin: langchain-mcp-adapters>=0.1.0
# Pin: langchain>=0.3.0, langgraph>=0.2.0

# GOTCHA: MultiServerMCPClient is an async context manager
# Must use: async with MultiServerMCPClient(config) as client:
# Cannot reuse client outside the context

# GOTCHA: create_react_agent requires a chat model, not a base LLM
# Use ChatOpenAI, ChatAnthropic, etc.
# For batch testing without an LLM, may need to call tools directly

# GOTCHA: Docker compose depends_on only waits for container start, not service ready
# Use healthcheck + condition: service_healthy for proper ordering

# GOTCHA: The CLI client needs network access to the MCP server
# In Docker: use service name "aviation-mcp" as hostname
# Outside Docker: use localhost:8000

# NOTE: For batch mode without an LLM, call MCP tools directly via
# the MCP client session rather than going through the LangChain agent
```

## Implementation Blueprint

### Data Models and Structure

```python
# === Test scenario definition ===
from dataclasses import dataclass

@dataclass
class TestScenario:
    name: str
    tool_name: str
    params: dict
    expected_check: str  # "non_empty", "empty", "contains_field"
    expected_value: str | None = None

# Predefined batch test scenarios
TEST_SCENARIOS = [
    # Flight status tests
    TestScenario("Flight lookup at BDL", "get_flight_status",
                 {"airport": "BDL"}, "non_empty"),
    TestScenario("Flight by number", "get_flight_status",
                 {"airport": "BDL", "flight_number": "1234"}, "non_empty"),
    TestScenario("Unknown airport returns empty", "get_flight_status",
                 {"airport": "XXX"}, "empty"),
    # Gate info tests
    TestScenario("Gates at JFK", "get_gate_info",
                 {"airport": "JFK"}, "non_empty"),
    TestScenario("Specific gate", "get_gate_info",
                 {"airport": "JFK", "gate_number": "A1"}, "non_empty"),
    TestScenario("Unknown gate returns empty", "get_gate_info",
                 {"airport": "JFK", "gate_number": "Z99"}, "empty"),
    # Weather tests
    TestScenario("Weather at LAX", "get_weather",
                 {"airport": "LAX"}, "non_empty"),
    TestScenario("Unknown airport weather", "get_weather",
                 {"airport": "XXX"}, "empty"),
]
```

### List of Tasks

```yaml
Task 1:
CREATE docker-compose.yml:
  - Define services: flight-status, gate-info, weather, aviation-mcp
  - Network: aviation-net (bridge)
  - Port mappings: 5001, 5002, 5003, 8000
  - Health checks for C# services (curl /api/flights, /api/gates, /api/weather)
  - aviation-mcp depends_on C# services with condition: service_healthy
  - Environment variables for service URLs passed to aviation-mcp
  - VERIFY: docker-compose config (validates syntax)

Task 2:
CREATE src/aviation-mcp-client/ project:
  - CREATE pyproject.toml with dependencies:
    - langchain>=0.3.0
    - langgraph>=0.2.0
    - langchain-mcp-adapters>=0.1.0
    - langchain-anthropic (or langchain-openai, configurable)
    - mcp>=1.25,<2
    - pytest (dev dependency)
    - pytest-asyncio (dev dependency)
  - RUN: cd src/aviation-mcp-client && uv sync

Task 3:
CREATE config module:
  - CREATE src/aviation-mcp-client/src/config.py
  - MCP server URL: MCP_SERVER_URL=http://localhost:8000/sse (default)
  - LLM provider config (API key env var, model name)
  - Batch mode flag

Task 4:
CREATE LangChain agent setup:
  - CREATE src/aviation-mcp-client/src/agent.py
  - Connect to MCP server via SSE using langchain-mcp-adapters
  - Load MCP tools via client.get_tools()
  - Create ReAct agent with create_react_agent(model, tools)
  - Return configured agent for use by REPL or batch runner

Task 5:
CREATE batch test runner:
  - CREATE src/aviation-mcp-client/src/test_runner.py
  - Define TEST_SCENARIOS list (as above)
  - Connect to MCP server directly (via mcp.client.sse.sse_client)
  - Call each tool with specified params
  - Validate response against expected_check
  - Print pass/fail per scenario
  - Return exit code 0 (all pass) or 1 (any fail)

Task 6:
CREATE CLI entry point:
  - CREATE src/aviation-mcp-client/src/client.py
  - Parse args: --test (batch mode), --mcp-url (server URL)
  - Default mode: interactive REPL
    - Prompt user for input
    - Send to LangChain agent
    - Display result
    - Loop until quit/exit
  - --test mode: run batch test runner
  - Handle Ctrl+C gracefully

Task 7:
CREATE pytest tests:
  - CREATE tests/test_client.py
  - Test batch test runner with mocked MCP responses
  - Test agent setup and tool loading
  - VERIFY: uv run pytest passes

Task 8:
INTEGRATION TEST:
  - RUN: docker-compose up --build
  - Wait for all services healthy
  - RUN: python client.py --test --mcp-url http://localhost:8000/sse
  - VERIFY: All batch scenarios pass
  - RUN: docker-compose down
```

### Per-Task Pseudocode

```python
# === client.py (CLI entry point) ===
import argparse
import asyncio
from src.agent import create_aviation_agent
from src.test_runner import run_batch_tests
from src.config import Config

async def interactive_mode(config: Config):
    agent = await create_aviation_agent(config)
    print("Aviation MCP Client (type 'quit' to exit)")
    while True:
        query = input("\n> ")
        if query.lower() in ("quit", "exit"):
            break
        result = await agent.ainvoke({"messages": [("user", query)]})
        # Print the last message (agent response)
        print(result["messages"][-1].content)

async def main():
    parser = argparse.ArgumentParser(description="Aviation MCP Test Client")
    parser.add_argument("--test", action="store_true", help="Run batch tests")
    parser.add_argument("--mcp-url", default="http://localhost:8000/sse")
    args = parser.parse_args()

    config = Config(mcp_url=args.mcp_url)

    if args.test:
        success = await run_batch_tests(config)
        raise SystemExit(0 if success else 1)
    else:
        await interactive_mode(config)

if __name__ == "__main__":
    asyncio.run(main())

# === agent.py ===
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

async def create_aviation_agent(config):
    client = MultiServerMCPClient({
        "aviation-mcp": {
            "url": config.mcp_url,
            "transport": "sse",
        }
    })
    async with client as c:
        tools = c.get_tools()
        model = config.get_chat_model()  # ChatAnthropic or ChatOpenAI
        agent = create_react_agent(model, tools)
        return agent

# === test_runner.py (batch mode — bypasses LLM, calls tools directly) ===
from mcp.client.sse import sse_client
from mcp import ClientSession

async def run_batch_tests(config) -> bool:
    async with sse_client(config.mcp_url) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            all_passed = True
            for scenario in TEST_SCENARIOS:
                result = await session.call_tool(scenario.tool_name, scenario.params)
                passed = check_result(result, scenario.expected_check, scenario.expected_value)
                status = "PASS" if passed else "FAIL"
                print(f"  [{status}] {scenario.name}")
                if not passed:
                    all_passed = False
            return all_passed
```

```yaml
# === docker-compose.yml ===
# version: "3.8"  # (deprecated field, omit for modern compose)
# services:
#   flight-status:
#     build:
#       context: ./src/flight-status
#       dockerfile: Dockerfile
#     ports: ["5001:5001"]
#     healthcheck:
#       test: ["CMD", "curl", "-f", "http://localhost:5001/api/flights"]
#       interval: 10s
#       timeout: 5s
#       retries: 5
#     networks: [aviation-net]
#
#   gate-info:
#     build: ./src/gate-info
#     ports: ["5002:5002"]
#     healthcheck: (similar)
#     networks: [aviation-net]
#
#   weather:
#     build: ./src/weather
#     ports: ["5003:5003"]
#     healthcheck: (similar)
#     networks: [aviation-net]
#
#   aviation-mcp:
#     build: ./src/aviation-mcp
#     ports: ["8000:8000"]
#     environment:
#       - FLIGHT_STATUS_URL=http://flight-status:5001
#       - GATE_INFO_URL=http://gate-info:5002
#       - WEATHER_URL=http://weather:5003
#       - MCP_DEBUG=true
#     depends_on:
#       flight-status: { condition: service_healthy }
#       gate-info: { condition: service_healthy }
#       weather: { condition: service_healthy }
#     networks: [aviation-net]
#
# networks:
#   aviation-net:
#     driver: bridge
```

### Integration Points

```yaml
UPSTREAM DEPENDENCIES:
  - MCP Server (Phase 2): SSE at http://aviation-mcp:8000/sse (Docker) or http://localhost:8000/sse (local)
  - Indirectly: C# services via MCP server tool calls

CONFIG:
  - MCP_SERVER_URL: MCP server SSE endpoint
  - LLM_PROVIDER: anthropic or openai (for interactive mode)
  - LLM_API_KEY: API key for chosen provider
  - LLM_MODEL: model name (e.g., claude-sonnet-4-5-20250929)

DOCKER:
  - docker-compose.yml at project root
  - Network: aviation-net connecting all services
  - Health checks on C# services for startup ordering
  - CLI client runs outside Docker (connects to localhost:8000)
```

## Validation Loop

### Level 1: Syntax & Style

```bash
# From src/aviation-mcp-client/
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# Expected: No errors
```

### Level 2: Unit Tests

```bash
# From src/aviation-mcp-client/
uv run pytest tests/ -v

# Expected: All tests pass
```

### Level 3: Integration Test

```bash
# From project root
docker-compose up --build -d

# Wait for health checks
docker-compose ps  # All services should show "healthy"

# Run batch tests
cd src/aviation-mcp-client
uv run src/client.py --test --mcp-url http://localhost:8000/sse

# Expected: All scenarios PASS, exit code 0

# Run interactive mode (manual test)
uv run src/client.py --mcp-url http://localhost:8000/sse
# Type: "What flights are at BDL?"
# Expected: Agent returns flight data

# Cleanup
docker-compose down
```

### Level 4: Debug Trace Verification

```bash
# Start with debug mode
docker-compose up --build -d

# Check MCP server logs for protocol trace
docker-compose logs aviation-mcp

# Expected: JSON-RPC messages, tool registration, capability negotiation visible
# Then run batch tests and verify request/response trace appears in logs
```

## Final Validation Checklist

- [ ] `docker-compose up --build` starts all 4 services
- [ ] All C# services pass health checks
- [ ] MCP server connects to all C# services
- [ ] CLI client connects to MCP server via SSE
- [ ] Batch mode: all test scenarios pass with exit code 0
- [ ] Interactive mode: natural language queries return aviation data
- [ ] Debug logs show full protocol trace (JSON-RPC, tool registration)
- [ ] `docker-compose down` cleans up cleanly
- [ ] pytest tests pass for client module
- [ ] Client handles MCP server unavailable gracefully

## Anti-Patterns to Avoid

- Do not require an LLM API key for batch testing — batch mode calls tools directly via MCP client
- Do not hardcode the MCP server URL — accept as CLI argument and env var
- Do not use synchronous HTTP clients — everything is async
- Do not skip health checks in docker-compose — services must be ready before dependent services start
- Do not run the CLI client inside Docker — it's a local development/testing tool

## Task Breakdown

See: [docs/tasks/phase3-cli-test-client.md](../tasks/phase3-cli-test-client.md)

---

**PRP Confidence Score: 7/10**

Good confidence for the docker-compose orchestration and batch testing (well-established patterns). Main risks: langchain-mcp-adapters SSE support may have version compatibility issues, interactive mode requires LLM API key configuration, and the agent REPL async loop needs careful implementation with input() blocking.
