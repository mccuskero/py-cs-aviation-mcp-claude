# PRP: Phase 2 — Python MCP Server

## Discovery Summary

### Initial Task Analysis

Build a Python MCP server using the official `mcp` Python SDK that exposes three tools (`get_flight_status`, `get_gate_info`, `get_weather`) as MCP protocol endpoints. Each tool proxies to the corresponding C# microservice from Phase 1 via HTTP REST. The server includes protocol-level debug logging to demonstrate MCP mechanics.

### User Clarifications Received

- **Question**: MCP SDK vs LangChain for the server?
- **Answer**: Official `mcp` Python SDK for the server; LangChain for the client (Phase 3)
- **Impact**: Server uses FastMCP from the mcp SDK, not LangChain

- **Question**: MCP transport type?
- **Answer**: SSE (Server-Sent Events)
- **Impact**: Server runs as HTTP service with SSE endpoint, suitable for Docker networking

- **Question**: Debug logging level?
- **Answer**: Protocol-level in debug mode (JSON-RPC framing, tool registration, capability negotiation)
- **Impact**: Custom protocol logger wrapping MCP SDK transport

### Missing Requirements Identified

- MCP SDK version pinning (resolved: `mcp>=1.25,<2` for v1.x stability)
- HTTP client library choice (resolved: `httpx` for async support)
- SSE is deprecated in MCP protocol v2025-03-26 in favor of Streamable HTTP; document this as future migration path

## Goal

Create a Python 3.13 MCP server using the official `mcp` SDK with SSE transport that registers three tools mapping to the Phase 1 C# microservices. The server provides protocol-level debug logging showing JSON-RPC message flow, tool registration, and capability negotiation. Object-oriented design with tool handler classes.

## Why

- Core component of the architectural demonstration — the bridge between AI agents and C# microservices
- Showcases MCP protocol mechanics (the primary focus area of the project)
- Demonstrates cross-language service communication (Python ↔ C# REST)
- Protocol debug logging makes the MCP handshake and tool invocation visible for educational purposes

## What

### User-visible Behavior

- MCP server starts and listens for SSE connections on port 8000
- Registers three tools: `get_flight_status`, `get_gate_info`, `get_weather`
- Each tool accepts parameters, calls the corresponding C# microservice, returns results
- Debug mode (`--debug` flag) logs full protocol-level details:
  - JSON-RPC message framing (requests/responses/notifications)
  - Tool registration and capability negotiation handshake
  - HTTP request/response to C# services
- Runs in Docker container alongside C# services

### Success Criteria

- [ ] MCP server starts and accepts SSE connections
- [ ] Three tools registered and discoverable via MCP protocol
- [ ] Each tool successfully calls its C# microservice and returns data
- [ ] Debug mode shows JSON-RPC messages, tool registration, and capability negotiation
- [ ] pytest tests pass for tool handlers and HTTP client layer
- [ ] Docker image builds and runs, can reach C# services on Docker network
- [ ] Server handles C# service errors gracefully (timeout, unavailable, empty results)

## All Needed Context

### Research Phase Summary

- **Codebase patterns found**: None (greenfield; Phase 1 C# services are the only dependency)
- **External research needed**: Yes — MCP Python SDK server setup, SSE transport, FastMCP tool registration
- **Knowledge gaps identified**: Protocol-level logging hooks in mcp SDK, SSE server configuration

**Key research findings:**

1. **MCP Python SDK v1.x** (`mcp>=1.25,<2`) is the stable production version. v2 is pre-alpha (Q1 2026).
2. **FastMCP** is the high-level server API within the SDK: `from mcp.server.fastmcp import FastMCP`
3. Tools are registered with `@mcp.tool()` decorator on async functions
4. **SSE transport**: Server runs as ASGI app via Starlette; SSE endpoint at `/sse`, messages at `/messages`
5. **SSE deprecation note**: SSE was deprecated in protocol v2025-03-26 in favor of Streamable HTTP. Both are supported in SDK v1.x. Migration path documented for future.
6. **Logging**: Python `logging` module can be configured to capture MCP protocol events

### Documentation & References

```yaml
- url: https://github.com/modelcontextprotocol/python-sdk
  why: Official SDK repository, server implementation patterns, FastMCP API

- url: https://modelcontextprotocol.github.io/python-sdk/
  why: SDK documentation, tool registration, transport configuration

- url: https://spec.modelcontextprotocol.io/
  why: MCP protocol specification — JSON-RPC framing, capability negotiation

- url: https://docs.astral.sh/uv/
  why: uv package manager for Python dependency management

- url: https://www.python-httpx.org/
  why: httpx async HTTP client for calling C# services

- file: docs/brainstorm/brainstorm-initialize-20260209.md
  why: Architecture decisions, risk register (MCP SDK stability)

- file: CLAUDE.md
  why: Project conventions, directory structure, service endpoints

- file: docs/prps/phase1-csharp-microservices.md
  why: C# service API contracts, port assignments, data models
```

### Current Codebase Tree (after Phase 1)

```
py-cs-aviation-mcp-claude/
├── src/
│   ├── flight-status/     # Phase 1: C# service on port 5001
│   ├── gate-info/         # Phase 1: C# service on port 5002
│   └── weather/           # Phase 1: C# service on port 5003
```

### Desired Codebase Tree (Phase 2 additions)

```
py-cs-aviation-mcp-claude/
├── src/
│   ├── aviation-mcp/
│   │   ├── Dockerfile
│   │   ├── pyproject.toml              # uv project config, dependencies
│   │   └── src/
│   │       ├── __init__.py
│   │       ├── server.py               # MCP server entry point, tool registration
│   │       ├── config.py               # Service URLs, port config, debug flag
│   │       ├── tools/
│   │       │   ├── __init__.py
│   │       │   ├── base.py             # Base tool handler class
│   │       │   ├── flight_status.py    # get_flight_status tool handler
│   │       │   ├── gate_info.py        # get_gate_info tool handler
│   │       │   └── weather.py          # get_weather tool handler
│   │       ├── clients/
│   │       │   ├── __init__.py
│   │       │   ├── base.py             # Base HTTP client class
│   │       │   ├── flight_status_client.py
│   │       │   ├── gate_info_client.py
│   │       │   └── weather_client.py
│   │       ├── models/
│   │       │   ├── __init__.py
│   │       │   ├── flight.py           # Pydantic models matching C# DTOs
│   │       │   ├── gate.py
│   │       │   └── weather.py
│   │       └── logging/
│   │           ├── __init__.py
│   │           └── protocol_logger.py  # Protocol-level debug logging
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── conftest.py             # Shared fixtures
│   │       ├── test_tools/
│   │       │   ├── __init__.py
│   │       │   ├── test_flight_status.py
│   │       │   ├── test_gate_info.py
│   │       │   └── test_weather.py
│   │       └── test_clients/
│   │           ├── __init__.py
│   │           ├── test_flight_status_client.py
│   │           ├── test_gate_info_client.py
│   │           └── test_weather_client.py
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: Pin MCP SDK to v1.x for stability
# mcp>=1.25,<2   (v2 is pre-alpha, breaking changes expected Q1 2026)

# CRITICAL: SSE transport is deprecated in MCP protocol v2025-03-26
# Still supported in SDK v1.x but Streamable HTTP is the replacement
# For this demo, SSE works fine. Migration to Streamable HTTP is straightforward:
#   SSE: mcp.run(transport="sse")
#   Streamable HTTP: mcp.run(transport="streamable-http")

# GOTCHA: FastMCP server runs on Starlette/uvicorn
# SSE endpoint is at /sse (GET), messages at /messages (POST)
# When running in Docker, bind to 0.0.0.0, not localhost

# GOTCHA: httpx async client must be used within async context
# Tool handlers are async functions, so httpx.AsyncClient fits naturally

# GOTCHA: MCP tool parameters are defined via function signatures + type hints
# The SDK uses inspect to generate JSON Schema from Python type hints
```

## Implementation Blueprint

### Data Models and Structure

```python
# === Pydantic models matching C# DTOs ===

from pydantic import BaseModel

class Flight(BaseModel):
    airport: str
    flight_number: str
    airline: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    status: str
    gate: str
    terminal: str

class Gate(BaseModel):
    airport: str
    gate_number: str
    terminal: str
    status: str
    assigned_flight: str | None
    airline: str | None
    last_updated: str

class AirportWeather(BaseModel):
    airport: str
    condition: str
    temperature_f: float
    temperature_c: float
    wind_speed: str
    visibility: str
    humidity: int
    last_updated: str
```

### List of Tasks

```yaml
Task 1:
CREATE src/aviation-mcp/ project structure:
  - CREATE pyproject.toml with dependencies:
    - mcp>=1.25,<2
    - httpx>=0.27
    - pydantic>=2.0
    - uvicorn
    - pytest (dev dependency)
    - pytest-asyncio (dev dependency)
    - pytest-httpx (dev dependency)
  - RUN: cd src/aviation-mcp && uv sync

Task 2:
CREATE config module:
  - CREATE src/aviation-mcp/src/config.py
  - Define service URLs (configurable via env vars):
    - FLIGHT_STATUS_URL=http://flight-status:5001
    - GATE_INFO_URL=http://gate-info:5002
    - WEATHER_URL=http://weather:5003
  - Define DEBUG flag (--debug CLI arg or MCP_DEBUG env var)

Task 3:
CREATE Pydantic models:
  - CREATE src/aviation-mcp/src/models/flight.py
  - CREATE src/aviation-mcp/src/models/gate.py
  - CREATE src/aviation-mcp/src/models/weather.py
  - MIRROR field names from C# DTOs (camelCase → snake_case mapping)

Task 4:
CREATE HTTP client classes:
  - CREATE src/aviation-mcp/src/clients/base.py (BaseServiceClient with httpx.AsyncClient)
  - CREATE flight_status_client.py, gate_info_client.py, weather_client.py
  - Each client: async method that calls C# service, returns parsed model list
  - HANDLE: connection errors, timeouts, non-200 responses

Task 5:
CREATE protocol logger:
  - CREATE src/aviation-mcp/src/logging/protocol_logger.py
  - Log JSON-RPC messages (method, params, id) when debug mode enabled
  - Log tool registration events
  - Log capability negotiation handshake
  - Log HTTP requests/responses to C# services
  - Use Python logging module with structured format

Task 6:
CREATE MCP tool handlers:
  - CREATE src/aviation-mcp/src/tools/base.py (base tool handler class)
  - CREATE flight_status.py, gate_info.py, weather.py
  - Each handler: accepts parameters, calls HTTP client, returns formatted result
  - OOP style: each tool is a class with an execute() method

Task 7:
CREATE MCP server entry point:
  - CREATE src/aviation-mcp/src/server.py
  - Initialize FastMCP("aviation-mcp")
  - Register three tools using @mcp.tool() decorator
  - Configure SSE transport
  - Wire up protocol logger for debug mode
  - Parse --debug CLI flag
  - RUN: uv run src/server.py to verify startup

Task 8:
CREATE pytest tests:
  - CREATE tests/conftest.py with shared fixtures (mock HTTP responses)
  - CREATE test_clients/ — test each HTTP client with mocked responses
  - CREATE test_tools/ — test each tool handler end-to-end with mocked clients
  - VERIFY: uv run pytest passes

Task 9:
CREATE Dockerfile:
  - Base image: python:3.13-slim
  - Install uv, copy pyproject.toml, run uv sync
  - Copy source code
  - EXPOSE 8000
  - ENTRYPOINT: uv run src/server.py
```

### Per-Task Pseudocode

```python
# === server.py (MCP server entry point) ===
import argparse
from mcp.server.fastmcp import FastMCP
from src.tools.flight_status import FlightStatusTool
from src.tools.gate_info import GateInfoTool
from src.tools.weather import WeatherTool
from src.logging.protocol_logger import setup_protocol_logging
from src.config import Config

mcp = FastMCP("aviation-mcp")
config = Config()

# Tool registration using @mcp.tool() decorator
@mcp.tool()
async def get_flight_status(airport: str = "", flight_number: str = "", time: str = "") -> str:
    """Get flight status information for an airport.

    Args:
        airport: IATA airport code (e.g., BDL, JFK)
        flight_number: Flight number (e.g., 1234)
        time: Departure time filter (ISO 8601 prefix)
    """
    tool = FlightStatusTool(config)
    return await tool.execute(airport=airport, flight_number=flight_number, time=time)

# Similar for get_gate_info and get_weather...

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        setup_protocol_logging()
    mcp.run(transport="sse")

# === clients/base.py ===
class BaseServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get(self, path: str, params: dict) -> list[dict]:
        # PATTERN: Filter out empty string params before sending
        filtered = {k: v for k, v in params.items() if v}
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}{path}", params=filtered, timeout=10.0)
            response.raise_for_status()
            return response.json()

# === logging/protocol_logger.py ===
# PATTERN: Configure Python logging to capture MCP SDK internals
# The mcp SDK uses Python logging — set level to DEBUG for protocol messages
import logging

def setup_protocol_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(name)s] %(message)s")
    # MCP SDK loggers
    logging.getLogger("mcp").setLevel(logging.DEBUG)
    logging.getLogger("mcp.server").setLevel(logging.DEBUG)
    # HTTP client logging
    logging.getLogger("httpx").setLevel(logging.DEBUG)
```

### Integration Points

```yaml
UPSTREAM DEPENDENCIES (Phase 1):
  - flight-status: http://flight-status:5001/api/flights
  - gate-info: http://gate-info:5002/api/gates
  - weather: http://weather:5003/api/weather
  - Service URLs configured via environment variables for Docker networking

CONFIG:
  - Environment variables: FLIGHT_STATUS_URL, GATE_INFO_URL, WEATHER_URL, MCP_DEBUG
  - CLI flag: --debug for protocol logging
  - pyproject.toml: all dependencies pinned

MCP PROTOCOL:
  - Transport: SSE (GET /sse for stream, POST /messages for client messages)
  - Port: 8000
  - Tools: get_flight_status, get_gate_info, get_weather
  - Protocol: JSON-RPC 2.0 over SSE
```

## Validation Loop

### Level 1: Syntax & Style

```bash
# From src/aviation-mcp/
uv run ruff check src/ tests/    # Linting
uv run ruff format src/ tests/   # Formatting

# Expected: No errors
```

### Level 2: Tests

```bash
# From src/aviation-mcp/
uv run pytest tests/ -v

# Expected: All tests pass
```

### Level 3: Manual Server Test

```bash
# Start server locally (requires Phase 1 services running)
cd src/aviation-mcp && uv run src/server.py --debug

# In another terminal, test with MCP Inspector
npx -y @modelcontextprotocol/inspector

# Connect to http://localhost:8000/sse and verify:
# 1. Three tools listed
# 2. Tool invocation returns data
# 3. Debug logs show JSON-RPC messages
```

## Final Validation Checklist

- [ ] `uv sync` installs all dependencies
- [ ] `uv run ruff check` passes (add ruff to dev deps)
- [ ] `uv run pytest` passes all tests
- [ ] Server starts with `uv run src/server.py`
- [ ] Debug mode shows protocol-level logs with `--debug` flag
- [ ] Three MCP tools registered and discoverable
- [ ] Each tool calls its C# service and returns formatted data
- [ ] Error handling works (C# service down → graceful error message)
- [ ] Docker image builds and runs
- [ ] Server reachable from Docker network on port 8000

## Anti-Patterns to Avoid

- Do not use `requests` library (synchronous) — use `httpx` for async compatibility
- Do not hardcode service URLs — use environment variables for Docker networking
- Do not catch all exceptions in tool handlers — let MCP SDK handle protocol-level errors
- Do not mix sync and async patterns — the MCP server is fully async

## Task Breakdown

See: [docs/tasks/phase2-python-mcp-server.md](../tasks/phase2-python-mcp-server.md)

---

**PRP Confidence Score: 7/10**

Good confidence with clear patterns from MCP SDK docs. Main risks: SSE deprecation (mitigated by v1.x support), protocol-level logging hooks may require custom implementation beyond basic Python logging, and httpx/mcp SDK async interaction needs testing.
