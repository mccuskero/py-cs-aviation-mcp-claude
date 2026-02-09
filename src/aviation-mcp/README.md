# Aviation MCP Server

Python MCP server that exposes three aviation tools over SSE (Server-Sent Events). Acts as the protocol bridge between MCP clients and the C# backend microservices.

## Architecture

```
MCP Client ──SSE──> FastMCP Server ──httpx──> C# Microservices
                     (port 8000)          (ports 5001-5003)
```

The server follows an OOP layered design:

```
server.py (tool registration)
  └── tools/ (tool handlers)
        └── clients/ (HTTP clients)
              └── models/ (Pydantic data models)
```

## Project Structure

```
src/aviation-mcp/
├── Dockerfile
├── pyproject.toml
└── src/
    ├── server.py                    # Entry point, FastMCP tool registration
    ├── config.py                    # Environment-based configuration
    ├── tools/
    │   ├── base.py                  # BaseTool abstract class
    │   ├── flight_status.py         # FlightStatusTool handler
    │   ├── gate_info.py             # GateInfoTool handler
    │   └── weather.py               # WeatherTool handler
    ├── clients/
    │   ├── base.py                  # BaseServiceClient (async httpx, 10s timeout)
    │   ├── flight_status_client.py  # GET /api/flights
    │   ├── gate_info_client.py      # GET /api/gates
    │   └── weather_client.py        # GET /api/weather
    ├── models/
    │   ├── flight.py                # Flight Pydantic model
    │   ├── gate.py                  # Gate Pydantic model
    │   └── weather.py               # AirportWeather Pydantic model
    └── debug_logging/
        └── protocol_logger.py       # JSON-RPC/MCP protocol debug logging
```

## MCP Tools

| Tool | Parameters | Returns |
|------|-----------|---------|
| `get_flight_status` | `airport` (IATA code), `flight_number`, `time` (ISO 8601) | Formatted flight status string |
| `get_gate_info` | `airport` (IATA code), `gate_number` | Formatted gate information string |
| `get_weather` | `airport` (IATA code) | Formatted weather conditions string |

All parameters are optional. Omitting a parameter returns all records (filtered only by provided parameters). Tools return human-readable formatted strings, not raw JSON.

## Running

### Local Development

```bash
uv sync
uv run src/server.py
```

The server starts on `http://0.0.0.0:8000` with SSE transport. The SSE endpoint is at `/sse`.

### With Debug Logging

```bash
uv run src/server.py --debug
```

Or set the environment variable:

```bash
MCP_DEBUG=true uv run src/server.py
```

Debug mode logs JSON-RPC message framing, MCP capability negotiation, tool registration events, and HTTP request/response details to stderr.

### Via Docker

```bash
docker build -t aviation-mcp .
docker run -p 8000:8000 \
  -e FLIGHT_STATUS_URL=http://host.docker.internal:5001 \
  -e GATE_INFO_URL=http://host.docker.internal:5002 \
  -e WEATHER_URL=http://host.docker.internal:5003 \
  -e MCP_DEBUG=true \
  aviation-mcp
```

### Via Docker Compose (from project root)

```bash
docker-compose up --build aviation-mcp
```

This starts the MCP server and all C# dependencies with proper health check ordering.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `FLIGHT_STATUS_URL` | `http://localhost:5001` | Flight status service base URL |
| `GATE_INFO_URL` | `http://localhost:5002` | Gate info service base URL |
| `WEATHER_URL` | `http://localhost:5003` | Weather service base URL |
| `MCP_DEBUG` | `false` | Enable protocol debug logging |

## Testing

```bash
uv run pytest tests/ -v
```

17 tests covering:
- **HTTP clients** (6 tests): Request construction, response parsing, empty param filtering
- **Tool handlers** (9 tests): Response formatting, empty results, service unavailability
- **Protocol logging** (2 tests): Debug output formatting

Tests use `pytest-httpx` to mock HTTP responses — no running C# services required.

## Dependencies

- `mcp>=1.25,<2` -- Official MCP SDK (FastMCP server)
- `httpx>=0.27` -- Async HTTP client for C# service calls
- `pydantic>=2.0` -- Data validation and model serialization
- `uvicorn` -- ASGI server

## Design Decisions

- **Tool handlers return formatted strings** rather than JSON, making responses more natural for LLM consumption in interactive mode.
- **BaseServiceClient filters empty parameters** before sending requests, so tools can accept optional params without polluting query strings.
- **Error handling returns user-friendly messages** instead of raising exceptions, keeping the MCP tool contract clean for clients.
- **`debug_logging/`** directory (not `logging/`) to avoid shadowing Python's stdlib `logging` module.
