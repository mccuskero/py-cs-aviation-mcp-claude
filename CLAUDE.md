# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Aviation MCP — an architectural pattern demonstration showing a Python MCP server calling C# backend microservices. The project showcases three focus areas: MCP protocol mechanics (with protocol-level debug logging), cross-language service communication (Python ↔ C#), and enterprise microservice structure.

The MCP server exposes three tools (`get_flight_status`, `get_gate_info`, `get_weather`) that proxy to C# REST microservices serving parameterized stubbed data from JSON files. A separate LangChain-based CLI client exercises the MCP server.

## Architecture

**Data flow:** LangChain CLI Client → MCP Server (Python, `mcp` SDK) → C# microservices (REST/Swagger)

```
py-cs-aviation-mcp-claude/
├── docker-compose.yml
├── src/
│   ├── aviation-mcp/               # Python MCP server
│   │   ├── Dockerfile
│   │   ├── pyproject.toml
│   │   └── src/
│   │       ├── server.py            # Entry point, tool registration
│   │       ├── tools/               # Tool handler classes (OOP)
│   │       │   ├── flight_status.py
│   │       │   ├── gate_info.py
│   │       │   └── weather.py
│   │       ├── clients/             # HTTP clients for C# services
│   │       │   ├── flight_status_client.py
│   │       │   ├── gate_info_client.py
│   │       │   └── weather_client.py
│   │       ├── models/              # Data models
│   │       └── logging/
│   │           └── protocol_logger.py  # JSON-RPC/MCP debug logging
│   ├── flight-status/               # C# microservice
│   │   ├── Dockerfile
│   │   └── src/
│   │       ├── FLIGHTSTATUS.CLI/       # ASP.NET Core entry point, Swagger config
│   │       ├── FLIGHTSTATUS.Core/      # Models, DTOs, interfaces
│   │       ├── FLIGHTSTATUS.Services/  # Business logic, JSON data loading
│   │       └── FLIGHTSTATUS.Tests/     # xUnit tests
│   ├── gate-info/                   # C# microservice (same layering)
│   └── weather/                     # C# microservice (same layering)
```

## Technology Stack & Key Decisions

| Component | Technology | Notes |
|-----------|-----------|-------|
| MCP Server | Python 3.13, official `mcp` SDK | Protocol-native; exposes tools over MCP |
| CLI Test Client | LangChain v1.2.6+ | Agent-native; connects to MCP server |
| Python packages | `uv` | `uv sync` to install, `uv run` to execute |
| Microservices | C# .NET 8, ASP.NET Core Controllers | Traditional `[ApiController]` pattern, not Minimal APIs |
| API docs | Swagger (Swashbuckle) | Each service has its own Swagger UI |
| Orchestration | Docker Compose | Per-service Dockerfiles |
| C# testing | xUnit | Service layer (data filtering) + controller layer (HTTP responses) |
| Python testing | pytest | Tool handlers + HTTP client layer |
| Integration testing | docker-compose + CLI client | Full chain exercise |

**Framework split rationale:** MCP SDK handles the server (protocol, tool registration, JSON-RPC transport) while LangChain handles the client (agent orchestration, tool invocation). Each framework in its ideal role.

## C# Microservice Pattern

All three services follow identical layering: **Controller → Service → Core**

- **CLI project:** ASP.NET Core entry point, `Program.cs`, Swagger configuration
- **Core project:** Models, DTOs, interfaces
- **Services project:** Business logic, JSON file loading, parameterized filtering
- **Tests project:** xUnit tests covering service + controller layers

Services load data from JSON files and filter by input parameters. Unknown parameters return HTTP 404.

## Service API Endpoints

- **flight-status:** `GET /api/flights?airport={code}&flightNumber={number}&time={time}`
- **gate-info:** `GET /api/gates?airport={code}&gateNumber={number}`
- **weather:** `GET /api/weather?airport={code}`

Stub data covers 3-5 airports with multiple records per service.

## Debug Logging

Protocol-level debug mode exposes:
- JSON-RPC message framing
- MCP tool registration and capability negotiation
- Request/response flow between MCP server and C# services

## Build & Run Commands

```bash
# Start all services
docker-compose up --build

# Start a single C# service
docker-compose up --build flight-status

# Python MCP server (from src/aviation-mcp/)
uv sync                    # install dependencies
uv run src/server.py       # run the server

# C# tests (from respective service src/ dirs)
dotnet test

# Python tests (from src/aviation-mcp/)
uv run pytest

# Full integration test
docker-compose up --build   # then run CLI client against the stack
```

## Project Phases

1. **Stubbed C# microservices** — .NET 8 Controller pattern, Swagger, parameterized JSON stubs, xUnit tests, Dockerfiles
2. **Python MCP server** — `mcp` SDK, tool handlers, HTTP clients, protocol debug logging, pytest
3. **CLI test client** — LangChain agent, docker-compose orchestration, end-to-end integration
