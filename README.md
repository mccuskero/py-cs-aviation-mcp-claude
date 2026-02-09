# Aviation MCP

A cross-language architecture demonstration: a Python MCP server calling C# backend microservices, with a LangChain CLI client for testing and interaction.

## Architecture

```
LangChain CLI Client ──SSE──> Python MCP Server ──HTTP──> C# Microservices ──> JSON Stubs
                                  (port 8000)         (ports 5001-5003)
```

The system has four services orchestrated via Docker Compose:

| Service | Language | Port | Purpose |
|---------|----------|------|---------|
| flight-status | C# / .NET 9 | 5001 | Flight status lookup by airport, flight number, time |
| gate-info | C# / .NET 9 | 5002 | Gate information by airport, gate number |
| weather | C# / .NET 9 | 5003 | Airport weather conditions |
| aviation-mcp | Python 3.13 | 8000 | MCP server exposing 3 tools over SSE |

The CLI client runs on the host machine and connects to the MCP server via SSE.

### Data Flow

1. **Client** sends a natural language query (interactive) or calls an MCP tool directly (batch)
2. **MCP Server** receives the tool call, translates it into an HTTP GET to the appropriate C# service
3. **C# Service** filters parameterized JSON stub data and returns results
4. **MCP Server** formats the response and returns it to the client

### MCP Tools

| Tool | Parameters | Description |
|------|-----------|-------------|
| `get_flight_status` | airport, flight_number, time | Flight status at an airport |
| `get_gate_info` | airport, gate_number | Gate information at an airport |
| `get_weather` | airport | Current weather conditions |

### Stub Data Coverage

Five airports: **BDL**, **JFK**, **LAX**, **ORD**, **ATL** with 3-4 records per service per airport.

## Project Structure

```
py-cs-aviation-mcp-claude/
├── docker-compose.yml              # Orchestrates all 4 services
├── src/
│   ├── aviation-mcp/               # Python MCP server
│   │   ├── Dockerfile
│   │   ├── pyproject.toml
│   │   └── src/
│   │       ├── server.py           # Entry point, tool registration
│   │       ├── config.py           # Environment-based configuration
│   │       ├── tools/              # MCP tool handlers (OOP)
│   │       ├── clients/            # Async HTTP clients for C# services
│   │       ├── models/             # Pydantic data models
│   │       └── debug_logging/      # JSON-RPC protocol logger
│   ├── aviation-mcp-client/        # LangChain CLI test client
│   │   ├── pyproject.toml
│   │   ├── src/
│   │   │   ├── client.py           # Entry point (REPL + batch modes)
│   │   │   ├── agent.py            # LangChain agent setup
│   │   │   ├── test_runner.py      # Batch test scenarios
│   │   │   └── config.py           # Client configuration
│   │   └── tests/
│   │       └── test_client.py      # 18 pytest unit tests
│   ├── flight-status/              # C# microservice (Controller -> Service -> Core)
│   │   ├── Dockerfile
│   │   └── src/
│   ├── gate-info/                  # C# microservice (same layering)
│   │   ├── Dockerfile
│   │   └── src/
│   └── weather/                    # C# microservice (same layering)
│       ├── Dockerfile
│       └── src/
```

## Quick Start

### Prerequisites

- **Docker** and **Docker Compose**
- **uv** (Python package manager) -- for running the CLI client
- **LLM API key** (optional, only for interactive mode)

### Start All Services

####

```bash
    # 1. Start all services
    docker-compose up --build -d

    # 2. Wait ~60s for health checks, then verify
    docker-compose ps

    # 3. Run batch tests (no LLM key needed)
    cd src/aviation-mcp-client
    uv run python -m src.client --test --mcp-url http://localhost:8000/sse

    # 4. (Optional) Interactive mode (needs ANTHROPIC_API_KEY or LLM_API_KEY)
    LLM_API_KEY=your-key uv run python -m src.client --mcp-url http://localhost:8000/sse

    # 5. Check debug logs
    docker-compose logs aviation-mcp

    # 6. Cleanup
    docker-compose down
```

####

```bash
docker-compose up --build -d
```

Wait for health checks (~60 seconds):

```bash
docker-compose ps
```

All C# services should show `healthy` before the MCP server starts.

### Run Batch Tests (No LLM Key Needed)

```bash
cd src/aviation-mcp-client
uv sync
uv run python -m src.client --test --mcp-url http://localhost:8000/sse
```

Runs 8 predefined test scenarios against all 3 tools. Exit code 0 = all pass.

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

### Interactive Mode (Requires LLM)

The interactive REPL needs a language model. Three providers are supported:

#### Anthropic (default)

```bash
LLM_API_KEY=your-anthropic-key uv run python -m src.client --mcp-url http://localhost:8000/sse
```

#### OpenAI

```bash
LLM_PROVIDER=openai LLM_MODEL=gpt-4o LLM_API_KEY=your-openai-key \
  uv run python -m src.client --mcp-url http://localhost:8000/sse
```

#### Ollama (local, no API key needed)

[Ollama](https://ollama.com) runs models locally and exposes an OpenAI-compatible API. No API key or cloud account required.

1. **Install Ollama** -- https://ollama.com/download

2. **Pull a model** with tool-calling support:

```bash
ollama pull llama3.2
```

Other models that support tool calling: `mistral`, `qwen2.5`, `command-r`. Check [Ollama model library](https://ollama.com/library) for the full list.

3. **Start the services** (if not already running):

```bash
docker-compose up --build -d
```

4. **Run the interactive client**:

```bash
LLM_PROVIDER=ollama LLM_MODEL=llama3.2 \
  uv run python -m src.client --mcp-url http://localhost:8000/sse
```

If Ollama runs on a different host or port:

```bash
LLM_PROVIDER=ollama LLM_MODEL=llama3.2 LLM_BASE_URL=http://myhost:11434/v1 \
  uv run python -m src.client --mcp-url http://localhost:8000/sse
```

```
Aviation MCP Client (type 'quit' to exit)
Connected to MCP server at http://localhost:8000/sse
Tools available: ['get_flight_status', 'get_gate_info', 'get_weather']

> What flights are at BDL?
```

### Check Debug Logs

```bash
docker-compose logs aviation-mcp
```

Shows JSON-RPC messages, tool registration, and request/response traces.

### Stop Services

```bash
docker-compose down
```

## Running Tests

### All Tests (68 total)

```bash
# C# microservice tests (30 xUnit tests)
cd src/flight-status/src && dotnet test
cd src/gate-info/src && dotnet test
cd src/weather/src && dotnet test

# Python MCP server tests (17 pytest tests)
cd src/aviation-mcp && uv run pytest

# Python CLI client tests (21 pytest tests)
cd src/aviation-mcp-client && uv run pytest
```

### Individual Service Tests

```bash
# Flight Status (11 tests)
cd src/flight-status/src && dotnet test --verbosity normal

# Gate Info (10 tests)
cd src/gate-info/src && dotnet test --verbosity normal

# Weather (9 tests)
cd src/weather/src && dotnet test --verbosity normal

# MCP Server (17 tests)
cd src/aviation-mcp && uv run pytest tests/ -v

# CLI Client (21 tests)
cd src/aviation-mcp-client && uv run pytest tests/ -v
```

## Technology Stack

| Component | Technology | Notes |
|-----------|-----------|-------|
| MCP Server | Python 3.13, `mcp` SDK (FastMCP) | SSE transport, async tool handlers |
| CLI Client | LangChain, LangGraph, `langchain-mcp-adapters` | ReAct agent for interactive mode |
| Microservices | C# .NET 9, ASP.NET Core Controllers | Traditional `[ApiController]` pattern |
| API Docs | Swagger (Swashbuckle) | Available at each service's `/swagger` endpoint |
| HTTP Client | httpx (async) | Python MCP server to C# services |
| Orchestration | Docker Compose | Health-check-based startup ordering |
| Python Packages | uv | Fast dependency management |
| C# Testing | xUnit | Service + controller layer tests |
| Python Testing | pytest, pytest-asyncio | Async mock-based unit tests |

## Configuration

### MCP Server Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLIGHT_STATUS_URL` | `http://localhost:5001` | Flight status service base URL |
| `GATE_INFO_URL` | `http://localhost:5002` | Gate info service base URL |
| `WEATHER_URL` | `http://localhost:5003` | Weather service base URL |
| `MCP_DEBUG` | `false` | Enable protocol debug logging |

### CLI Client Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_SERVER_URL` | `http://localhost:8000/sse` | MCP server SSE endpoint |
| `LLM_PROVIDER` | `anthropic` | LLM provider (`anthropic`, `openai`, or `ollama`) |
| `LLM_MODEL` | `claude-sonnet-4-5-20250929` | Model name |
| `LLM_API_KEY` | (none) | API key (not needed for Ollama) |
| `LLM_BASE_URL` | (none) | Custom API base URL (Ollama default: `http://localhost:11434/v1`) |

### CLI Arguments

```
python -m src.client [--test] [--mcp-url URL]

  --test       Run batch tests instead of interactive REPL
  --mcp-url    Override MCP server SSE URL
```

## Docker Compose Services

```yaml
flight-status:  5001  # Health check: GET /api/flights
gate-info:      5002  # Health check: GET /api/gates
weather:        5003  # Health check: GET /api/weather
aviation-mcp:   8000  # Depends on all 3 C# services being healthy
```

All services communicate over the `aviation-net` bridge network. The MCP server waits for all C# service health checks to pass before starting.
