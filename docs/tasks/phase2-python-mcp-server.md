# Task Breakdown: Phase 2 -- Python MCP Server

> **Source PRP**: [docs/prps/phase2-python-mcp-server.md](/docs/prps/phase2-python-mcp-server.md)
> **Generated**: 2026-02-09
> **Overall Complexity**: Moderate
> **Total Tasks**: 9
> **Phases**: 3 (Foundation, Core Implementation, Integration & Packaging)

---

## PRP Analysis Summary

**Feature**: Python MCP server using the official `mcp` SDK (v1.x) with SSE transport, exposing three aviation tools (`get_flight_status`, `get_gate_info`, `get_weather`) that proxy to Phase 1 C# microservices via HTTP REST.

**Key Technical Requirements**:
- Python 3.13, `mcp>=1.25,<2` SDK with FastMCP server API
- SSE transport (GET `/sse`, POST `/messages`) on port 8000
- OOP tool handler classes with async `execute()` methods
- `httpx` async HTTP clients calling C# services on ports 5001/5002/5003
- Pydantic v2 models mirroring C# DTOs (camelCase to snake_case mapping)
- Protocol-level debug logging (JSON-RPC messages, tool registration, capability negotiation)
- `uv` for dependency management, pytest for testing, Docker for deployment

**Validation Requirements**:
- `uv run ruff check` and `uv run ruff format` pass with no errors
- `uv run pytest` passes all tests
- Server starts and accepts SSE connections
- Three tools registered and discoverable via MCP protocol
- Each tool successfully calls its C# microservice and returns data
- Debug mode shows JSON-RPC messages, tool registration, and capability negotiation
- Docker image builds and runs, can reach C# services on Docker network
- Server handles C# service errors gracefully (timeout, unavailable, empty results)

---

## Task Complexity Assessment

**Overall Complexity**: Moderate

| Factor | Rating | Notes |
|--------|--------|-------|
| Technical novelty | Moderate | MCP SDK is well-documented; FastMCP API is straightforward |
| Integration points | Moderate | 3 upstream C# services, Docker networking |
| Async complexity | Low-Moderate | httpx async fits naturally with MCP async tool handlers |
| Testing complexity | Moderate | Mocking HTTP clients, async test fixtures |
| Protocol logging | Moderate | Python logging hooks into MCP SDK internals |

**Integration Points**:
- Phase 1 C# services: `flight-status:5001`, `gate-info:5002`, `weather:5003`
- MCP protocol: JSON-RPC 2.0 over SSE transport
- Docker network for inter-service communication
- Environment variables for service URL configuration

**Technical Challenges**:
- Correct async lifecycle management for httpx clients within MCP tool handlers
- Protocol-level logging hooks in the mcp SDK (may require configuring SDK-internal loggers)
- SSE transport is deprecated in MCP protocol v2025-03-26 (still supported in SDK v1.x)
- camelCase to snake_case field mapping between C# DTOs and Pydantic models

---

## Phase Organization

### Phase 1: Foundation (Tasks 1-3)
**Objective**: Establish project structure, configuration, and data models.
**Deliverables**: Working `uv` project, configuration module, Pydantic models.
**Milestone**: `uv sync` succeeds, models importable, config loads from env vars.

### Phase 2: Core Implementation (Tasks 4-7)
**Objective**: Build the HTTP clients, protocol logger, tool handlers, and MCP server entry point.
**Deliverables**: Working MCP server that registers 3 tools, calls C# services, returns data.
**Milestone**: `uv run src/server.py --debug` starts and tools are invocable via MCP Inspector.

### Phase 3: Quality & Packaging (Tasks 8-9)
**Objective**: Add tests and Docker packaging.
**Deliverables**: Full pytest suite, production-ready Docker image.
**Milestone**: `uv run pytest` passes, Docker image builds and runs on the Docker network.

---

## Detailed Task Breakdown

---

### T-001: Create Project Structure and Dependencies

**Task ID**: T-001
**Task Name**: Create `src/aviation-mcp/` project structure with `pyproject.toml` and `uv` setup
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase2-python-mcp-server.md](/docs/prps/phase2-python-mcp-server.md) -- Task 1

##### Feature Overview
This is the foundational scaffolding task for the Python MCP server. All subsequent tasks depend on this project structure and dependency resolution being in place.

##### Task Purpose
**As a** developer
**I need** a properly configured Python 3.13 project with all dependencies resolved
**So that** subsequent tasks can import libraries and follow the established directory structure

##### Dependencies
- **Prerequisite Tasks**: None (first task in Phase 2)
- **Parallel Tasks**: None
- **Integration Points**: Phase 1 C# services must exist (for later integration)
- **Blocked By**: Nothing

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When `uv sync` is run in `src/aviation-mcp/`, all dependencies install without error
- **REQ-2**: The directory structure matches the desired codebase tree from the PRP
- **REQ-3**: When Python files are created in `src/`, they are importable as a package

##### Non-Functional Requirements
- **Performance**: N/A (setup task)
- **Security**: Pin dependency versions to prevent supply chain issues

##### Technical Constraints
- **Technology Stack**: Python 3.13, `uv` package manager
- **Dependencies**: `mcp>=1.25,<2`, `httpx>=0.27`, `pydantic>=2.0`, `uvicorn`
- **Dev Dependencies**: `pytest`, `pytest-asyncio`, `pytest-httpx`, `ruff`

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp/
├── pyproject.toml                    - Project metadata, dependencies, tool config
├── src/
│   ├── __init__.py                   - Package init (empty)
│   ├── tools/
│   │   └── __init__.py               - Package init (empty)
│   ├── clients/
│   │   └── __init__.py               - Package init (empty)
│   ├── models/
│   │   └── __init__.py               - Package init (empty)
│   └── logging/
│       └── __init__.py               - Package init (empty)
└── tests/
    ├── __init__.py                   - Package init (empty)
    ├── test_tools/
    │   └── __init__.py               - Package init (empty)
    └── test_clients/
        └── __init__.py               - Package init (empty)
```

##### Key Implementation Steps
1. **Create directory tree** with all subdirectories and `__init__.py` files -> Importable package hierarchy
2. **Create `pyproject.toml`** with `[project]` metadata, dependencies, and `[tool.ruff]` config -> Dependency manifest
3. **Run `uv sync`** to resolve and install all dependencies -> Lock file generated, venv populated

##### Code Patterns to Follow
```toml
# pyproject.toml pattern
[project]
name = "aviation-mcp"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "mcp>=1.25,<2",
    "httpx>=0.27",
    "pydantic>=2.0",
    "uvicorn",
]

[dependency-groups]
dev = [
    "pytest",
    "pytest-asyncio",
    "pytest-httpx",
    "ruff",
]

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Dependency installation succeeds
  Given the pyproject.toml is created with all required dependencies
  When uv sync is run in the src/aviation-mcp/ directory
  Then all dependencies install without errors
  And a uv.lock file is generated

Scenario 2: Package structure is importable
  Given all __init__.py files are in place
  When Python is invoked from the project root
  Then "from src.models import *" does not raise ImportError
  And "from src.tools import *" does not raise ImportError

Scenario 3: Dev tools are available
  Given dev dependencies are installed
  When uv run ruff check is invoked
  Then ruff executes without "command not found" error
```

##### Rule-Based Criteria (Checklist)
- [ ] `pyproject.toml` exists with correct dependencies and version pins
- [ ] All directories have `__init__.py` files
- [ ] `uv sync` completes without errors
- [ ] `uv.lock` is generated
- [ ] `uv run ruff check src/` executes (may show warnings on empty files, but no crash)
- [ ] Directory structure matches the PRP desired codebase tree

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp
uv sync
uv run ruff check src/ tests/
```

##### Definition of Done
- [ ] All files created per the directory tree above
- [ ] `uv sync` succeeds
- [ ] `uv run python -c "from src import tools, clients, models, logging"` succeeds

#### Resources & References

##### Documentation Links
- **uv docs**: https://docs.astral.sh/uv/ -- Project setup, `pyproject.toml` format
- **MCP SDK**: https://github.com/modelcontextprotocol/python-sdk -- Version requirements

#### Notes & Comments

##### Implementation Notes
- The `logging/` directory name shadows Python's built-in `logging` module. Use absolute imports throughout (e.g., `from src.logging.protocol_logger import ...`) to avoid collision. Alternatively, consider renaming to `debug_logging/` if import issues arise, but the PRP specifies `logging/` so start with that.
- `uv` will create a `.venv/` directory; ensure `.gitignore` excludes it.

---

### T-002: Create Configuration Module

**Task ID**: T-002
**Task Name**: Create configuration module with environment variables and CLI debug flag
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase2-python-mcp-server.md](/docs/prps/phase2-python-mcp-server.md) -- Task 2

##### Feature Overview
Centralized configuration for service URLs and debug mode. All HTTP clients and the server entry point depend on this module for runtime configuration.

##### Task Purpose
**As a** developer
**I need** a configuration module that reads service URLs from environment variables and supports a debug flag
**So that** the server can locate C# services in both local development and Docker environments

##### Dependencies
- **Prerequisite Tasks**: T-001 (project structure)
- **Parallel Tasks**: T-003 (Pydantic models) -- no dependency between them
- **Integration Points**: Docker Compose environment variables, CLI argument parsing
- **Blocked By**: Nothing

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When environment variable `FLIGHT_STATUS_URL` is set, the config returns that value
- **REQ-2**: When no environment variable is set, the config returns sensible defaults for local development
- **REQ-3**: When `--debug` flag or `MCP_DEBUG=true` env var is provided, debug mode is enabled

##### Technical Constraints
- **Defaults**: `FLIGHT_STATUS_URL=http://localhost:5001`, `GATE_INFO_URL=http://localhost:5002`, `WEATHER_URL=http://localhost:5003`
- **Docker overrides**: `http://flight-status:5001`, `http://gate-info:5002`, `http://weather:5003`

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp/src/config.py    - Configuration class with env var loading
```

##### Key Implementation Steps
1. **Create `Config` class** that reads env vars with defaults -> Centralized config object
2. **Add `debug` property** that checks `MCP_DEBUG` env var -> Debug mode support
3. **Add service URL properties** for each C# service -> URL resolution

##### Code Patterns to Follow
```python
# config.py pattern
import os

class Config:
    """Server configuration loaded from environment variables."""

    def __init__(self):
        self.flight_status_url: str = os.getenv(
            "FLIGHT_STATUS_URL", "http://localhost:5001"
        )
        self.gate_info_url: str = os.getenv(
            "GATE_INFO_URL", "http://localhost:5002"
        )
        self.weather_url: str = os.getenv(
            "WEATHER_URL", "http://localhost:5003"
        )
        self.debug: bool = os.getenv("MCP_DEBUG", "false").lower() == "true"
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Default configuration
  Given no environment variables are set
  When Config() is instantiated
  Then flight_status_url equals "http://localhost:5001"
  And gate_info_url equals "http://localhost:5002"
  And weather_url equals "http://localhost:5003"
  And debug is False

Scenario 2: Environment variable override
  Given FLIGHT_STATUS_URL is set to "http://flight-status:5001"
  When Config() is instantiated
  Then flight_status_url equals "http://flight-status:5001"

Scenario 3: Debug mode via environment
  Given MCP_DEBUG is set to "true"
  When Config() is instantiated
  Then debug is True
```

##### Rule-Based Criteria (Checklist)
- [ ] Config class loads all three service URLs from environment variables
- [ ] Default values point to localhost with correct ports (5001, 5002, 5003)
- [ ] Debug flag reads from `MCP_DEBUG` environment variable
- [ ] Config is importable from `src.config`

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp
uv run ruff check src/config.py
uv run python -c "from src.config import Config; c = Config(); print(c.flight_status_url)"
```

##### Definition of Done
- [ ] `config.py` created and importable
- [ ] All three service URLs configurable via env vars
- [ ] Debug flag supported via env var
- [ ] Default values work for local development

---

### T-003: Create Pydantic Data Models

**Task ID**: T-003
**Task Name**: Create Pydantic models matching C# DTOs for flights, gates, and weather
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase2-python-mcp-server.md](/docs/prps/phase2-python-mcp-server.md) -- Task 3

##### Feature Overview
Pydantic v2 models that mirror the C# DTOs returned by the Phase 1 microservices. These models provide type-safe deserialization of JSON responses from the C# services, with camelCase to snake_case field mapping.

##### Task Purpose
**As a** developer
**I need** Pydantic models that match the C# service response schemas
**So that** HTTP client responses are parsed into typed Python objects with validation

##### Dependencies
- **Prerequisite Tasks**: T-001 (project structure)
- **Parallel Tasks**: T-002 (config) -- no dependency between them
- **Integration Points**: C# service JSON response schemas (Phase 1)
- **Blocked By**: Nothing

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When a JSON response from the flight-status service is parsed, all fields map correctly
- **REQ-2**: When C# returns camelCase field names, Pydantic models accept them via alias configuration
- **REQ-3**: When optional fields are null/missing in the response, the model handles them gracefully

##### Technical Constraints
- **Library**: Pydantic v2 (`pydantic>=2.0`)
- **Field mapping**: C# uses camelCase, Python uses snake_case; use Pydantic `model_config` with `populate_by_name=True` and `alias_generator`

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp/src/models/
├── __init__.py        - Re-export all models
├── flight.py          - Flight model
├── gate.py            - Gate model
└── weather.py         - AirportWeather model
```

##### Key Implementation Steps
1. **Create `Flight` model** in `flight.py` matching C# DTO fields -> Type-safe flight data
2. **Create `Gate` model** in `gate.py` matching C# DTO fields -> Type-safe gate data
3. **Create `AirportWeather` model** in `weather.py` matching C# DTO fields -> Type-safe weather data
4. **Configure camelCase alias support** in each model -> C# JSON compatibility
5. **Update `__init__.py`** to re-export all models -> Clean import paths

##### Code Patterns to Follow
```python
# models/flight.py pattern
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class Flight(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

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
```

##### API Specifications (upstream C# response shapes)
```yaml
# Flight Status response shape
GET /api/flights?airport=BDL
Response: 200
Body: [
  {
    "airport": "BDL",
    "flightNumber": "1234",
    "airline": "Delta",
    "origin": "BDL",
    "destination": "JFK",
    "departureTime": "2026-02-09T08:00:00",
    "arrivalTime": "2026-02-09T10:00:00",
    "status": "On Time",
    "gate": "A1",
    "terminal": "A"
  }
]

# Gate Info response shape
GET /api/gates?airport=BDL
Response: 200
Body: [
  {
    "airport": "BDL",
    "gateNumber": "A1",
    "terminal": "A",
    "status": "Occupied",
    "assignedFlight": "DL1234",
    "airline": "Delta",
    "lastUpdated": "2026-02-09T08:00:00"
  }
]

# Weather response shape
GET /api/weather?airport=BDL
Response: 200
Body: [
  {
    "airport": "BDL",
    "condition": "Partly Cloudy",
    "temperatureF": 45.0,
    "temperatureC": 7.2,
    "windSpeed": "15 mph NW",
    "visibility": "10 miles",
    "humidity": 55,
    "lastUpdated": "2026-02-09T08:00:00"
  }
]
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Parse camelCase flight JSON
  Given a JSON dict with camelCase keys from the flight-status service
  When Flight(**json_dict) is called
  Then a Flight object is created with snake_case attribute names
  And flight.flight_number equals the "flightNumber" value from JSON

Scenario 2: Parse gate with optional fields
  Given a JSON dict where "assignedFlight" is null
  When Gate(**json_dict) is called
  Then gate.assigned_flight is None

Scenario 3: Parse weather with numeric fields
  Given a JSON dict with temperatureF as 45.0 and humidity as 55
  When AirportWeather(**json_dict) is called
  Then weather.temperature_f equals 45.0
  And weather.humidity equals 55
```

##### Rule-Based Criteria (Checklist)
- [ ] `Flight` model has all 10 fields matching the C# DTO
- [ ] `Gate` model has all 7 fields with `assigned_flight` and `airline` as optional (`str | None`)
- [ ] `AirportWeather` model has all 8 fields with correct types (float for temps, int for humidity)
- [ ] All models support both camelCase (JSON alias) and snake_case (Python attribute) access
- [ ] Models are re-exported from `src.models.__init__`

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp
uv run ruff check src/models/
uv run python -c "
from src.models.flight import Flight
f = Flight(airport='BDL', flightNumber='1234', airline='Delta', origin='BDL',
           destination='JFK', departureTime='2026-02-09T08:00:00',
           arrivalTime='2026-02-09T10:00:00', status='On Time', gate='A1', terminal='A')
print(f.flight_number)  # Should print '1234'
"
```

##### Definition of Done
- [ ] All three model files created
- [ ] camelCase alias support verified
- [ ] Optional fields handled correctly
- [ ] `__init__.py` exports all models

#### Resources & References

##### Documentation Links
- **Pydantic v2 docs**: https://docs.pydantic.dev/latest/ -- Model configuration, alias generators
- **Phase 1 PRP**: [docs/prps/phase1-csharp-microservices.md](/docs/prps/phase1-csharp-microservices.md) -- C# DTO field definitions

---

### T-004: Create HTTP Client Classes

**Task ID**: T-004
**Task Name**: Create async HTTP client classes for C# microservice communication
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase2-python-mcp-server.md](/docs/prps/phase2-python-mcp-server.md) -- Task 4

##### Feature Overview
Async HTTP client layer using `httpx` to call the three Phase 1 C# microservices. Each client has a base class providing shared HTTP logic (timeouts, error handling, response parsing) and a specialized subclass per service.

##### Task Purpose
**As a** tool handler
**I need** async HTTP clients that call C# services and return parsed Pydantic models
**So that** MCP tool invocations translate into correct REST API calls with typed responses

##### Dependencies
- **Prerequisite Tasks**: T-001 (project structure), T-002 (config), T-003 (Pydantic models)
- **Parallel Tasks**: T-005 (protocol logger) -- no dependency
- **Integration Points**: Phase 1 C# services (REST APIs)
- **Blocked By**: Nothing

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When a client method is called with query parameters, it sends a GET request to the correct C# service endpoint with those parameters
- **REQ-2**: When the C# service returns a JSON array, the client parses it into a list of Pydantic models
- **REQ-3**: When the C# service is unreachable, the client raises a descriptive error
- **REQ-4**: When query parameters are empty strings, they are filtered out before sending

##### Non-Functional Requirements
- **Performance**: HTTP timeout of 10 seconds per request
- **Error Handling**: Connection errors, timeouts, non-200 responses all produce clear error messages

##### Technical Constraints
- **Library**: `httpx>=0.27` with `httpx.AsyncClient`
- **Pattern**: Async context manager for client lifecycle; create client per request (simple) or share via dependency injection

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp/src/clients/
├── __init__.py                    - Re-export client classes
├── base.py                        - BaseServiceClient with shared HTTP logic
├── flight_status_client.py        - FlightStatusClient
├── gate_info_client.py            - GateInfoClient
└── weather_client.py              - WeatherClient
```

##### Key Implementation Steps
1. **Create `BaseServiceClient`** with `base_url`, async `get()` method, empty-param filtering, timeout config -> Shared HTTP logic
2. **Create `FlightStatusClient`** extending base, with `get_flights(airport, flight_number, time)` -> Typed flight queries
3. **Create `GateInfoClient`** extending base, with `get_gates(airport, gate_number)` -> Typed gate queries
4. **Create `WeatherClient`** extending base, with `get_weather(airport)` -> Typed weather queries
5. **Add error handling** for `httpx.ConnectError`, `httpx.TimeoutException`, `httpx.HTTPStatusError` -> Graceful degradation

##### Code Patterns to Follow
```python
# clients/base.py pattern
import httpx
import logging

logger = logging.getLogger(__name__)

class BaseServiceClient:
    """Base HTTP client for C# microservice communication."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get(self, path: str, params: dict) -> list[dict]:
        """Send GET request with filtered params, return JSON response."""
        filtered = {k: v for k, v in params.items() if v}
        async with httpx.AsyncClient() as client:
            logger.debug("GET %s%s params=%s", self.base_url, path, filtered)
            response = await client.get(
                f"{self.base_url}{path}",
                params=filtered,
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()

# clients/flight_status_client.py pattern
from src.clients.base import BaseServiceClient
from src.models.flight import Flight

class FlightStatusClient(BaseServiceClient):
    """HTTP client for the flight-status C# microservice."""

    def __init__(self, base_url: str):
        super().__init__(base_url)

    async def get_flights(
        self, airport: str = "", flight_number: str = "", time: str = ""
    ) -> list[Flight]:
        data = await self.get("/api/flights", {
            "airport": airport,
            "flightNumber": flight_number,
            "time": time,
        })
        return [Flight(**item) for item in data]
```

##### API Specifications (upstream C# endpoints)
```yaml
# Flight Status
Method: GET
Path: /api/flights
Params: airport (string), flightNumber (string), time (string)
Response: 200, body: Flight[]

# Gate Info
Method: GET
Path: /api/gates
Params: airport (string), gateNumber (string)
Response: 200, body: Gate[]

# Weather
Method: GET
Path: /api/weather
Params: airport (string)
Response: 200, body: AirportWeather[]
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Successful flight query
  Given the flight-status service is running on port 5001
  When FlightStatusClient.get_flights(airport="BDL") is called
  Then a list of Flight objects is returned
  And each Flight has a valid airport field

Scenario 2: Empty parameters are filtered
  Given a client call with airport="BDL" and flight_number=""
  When the HTTP request is sent
  Then the query string contains only "airport=BDL"
  And flight_number is not included in the query

Scenario 3: Service unavailable
  Given the C# service is not running
  When a client method is called
  Then an httpx.ConnectError is raised with a descriptive message

Scenario 4: Request timeout
  Given the C# service takes longer than 10 seconds to respond
  When a client method is called
  Then an httpx.TimeoutException is raised
```

##### Rule-Based Criteria (Checklist)
- [ ] `BaseServiceClient` provides shared `get()` method with param filtering and timeout
- [ ] `FlightStatusClient` calls `/api/flights` with correct query parameter names (camelCase)
- [ ] `GateInfoClient` calls `/api/gates` with correct query parameter names
- [ ] `WeatherClient` calls `/api/weather` with correct query parameter names
- [ ] All clients return lists of typed Pydantic models
- [ ] Error handling covers connection errors, timeouts, and non-200 responses
- [ ] Logging of HTTP requests/responses at DEBUG level

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp
uv run ruff check src/clients/
```

##### Definition of Done
- [ ] All four client files created (base + 3 service-specific)
- [ ] Empty parameter filtering works
- [ ] Error handling covers all httpx exception types
- [ ] Clients parse responses into Pydantic models
- [ ] Debug logging of HTTP requests

#### Resources & References

##### Documentation Links
- **httpx docs**: https://www.python-httpx.org/ -- AsyncClient, error handling, timeouts
- **Phase 1 PRP**: [docs/prps/phase1-csharp-microservices.md](/docs/prps/phase1-csharp-microservices.md) -- API endpoint contracts

---

### T-005: Create Protocol Debug Logger

**Task ID**: T-005
**Task Name**: Create protocol-level debug logging for MCP JSON-RPC messages and service calls
**Priority**: High

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase2-python-mcp-server.md](/docs/prps/phase2-python-mcp-server.md) -- Task 5

##### Feature Overview
Protocol-level debug logging is a primary focus of this project -- making the MCP handshake, tool registration, and JSON-RPC message flow visible for educational purposes. This logger hooks into the MCP SDK's Python logging hierarchy and the httpx client logging.

##### Task Purpose
**As a** developer or learner
**I need** detailed protocol-level logs showing MCP JSON-RPC messages, tool registration, and capability negotiation
**So that** the MCP protocol mechanics are visible and understandable

##### Dependencies
- **Prerequisite Tasks**: T-001 (project structure)
- **Parallel Tasks**: T-004 (HTTP clients) -- no dependency
- **Integration Points**: MCP SDK internal loggers, httpx loggers, Python `logging` module
- **Blocked By**: Nothing

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When debug mode is enabled, JSON-RPC messages (method, params, id) are logged
- **REQ-2**: When debug mode is enabled, tool registration events are logged
- **REQ-3**: When debug mode is enabled, capability negotiation handshake details are logged
- **REQ-4**: When debug mode is enabled, HTTP requests/responses to C# services are logged
- **REQ-5**: When debug mode is NOT enabled, only standard INFO-level logs appear

##### Technical Constraints
- **Library**: Python `logging` module
- **Pattern**: Configure MCP SDK loggers (`mcp`, `mcp.server`) to DEBUG level; configure httpx logger to DEBUG level
- **Format**: Structured log format with timestamps, logger names, and message content

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp/src/logging/
├── __init__.py              - Re-export setup function
└── protocol_logger.py       - Protocol logging configuration
```

##### Key Implementation Steps
1. **Create `setup_protocol_logging()` function** that configures all relevant loggers -> Debug mode activation
2. **Configure MCP SDK loggers** (`mcp`, `mcp.server`) to DEBUG level -> JSON-RPC message visibility
3. **Configure httpx logger** to DEBUG level -> HTTP request/response visibility
4. **Set structured log format** with timestamps and logger names -> Readable output
5. **Add custom log filter or handler** if needed for additional protocol context -> Enhanced debugging

##### Code Patterns to Follow
```python
# logging/protocol_logger.py pattern
import logging
import sys

def setup_protocol_logging() -> None:
    """Enable protocol-level debug logging for MCP and HTTP communication.

    Configures Python logging to capture:
    - MCP SDK JSON-RPC messages (tool registration, capability negotiation)
    - HTTP request/response details to C# services
    """
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # MCP SDK loggers
    for logger_name in ("mcp", "mcp.server", "mcp.server.fastmcp"):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    # HTTP client logging
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.DEBUG)
    httpx_logger.addHandler(handler)

    # Application logging
    app_logger = logging.getLogger("aviation_mcp")
    app_logger.setLevel(logging.DEBUG)
    app_logger.addHandler(handler)

    app_logger.info("Protocol debug logging enabled")
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Debug mode shows MCP protocol messages
  Given the server is started with --debug flag
  When an MCP client connects and performs capability negotiation
  Then the log output shows JSON-RPC messages with method names and params

Scenario 2: Debug mode shows HTTP client activity
  Given the server is started with --debug flag
  When a tool invocation triggers an HTTP call to a C# service
  Then the log output shows the HTTP GET URL, parameters, and response status

Scenario 3: Normal mode suppresses debug output
  Given the server is started without --debug flag
  When an MCP client connects and invokes tools
  Then no DEBUG-level log messages appear in output
```

##### Rule-Based Criteria (Checklist)
- [ ] `setup_protocol_logging()` function exists and is callable
- [ ] MCP SDK loggers configured to DEBUG level when enabled
- [ ] httpx logger configured to DEBUG level when enabled
- [ ] Log format includes timestamp, logger name, level, and message
- [ ] Function is idempotent (calling twice does not duplicate handlers)
- [ ] Application logger (`aviation_mcp`) available for tool/client logging

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp
uv run ruff check src/logging/
uv run python -c "from src.logging.protocol_logger import setup_protocol_logging; setup_protocol_logging()"
```

##### Definition of Done
- [ ] `protocol_logger.py` created and importable
- [ ] `setup_protocol_logging()` configures all required loggers
- [ ] Log format is structured and readable
- [ ] No debug output when debug mode is not enabled

#### Resources & References

##### Documentation Links
- **MCP SDK**: https://github.com/modelcontextprotocol/python-sdk -- Logger names used by the SDK
- **Python logging**: https://docs.python.org/3/library/logging.html -- Configuration patterns

##### Implementation Notes
- The exact logger names used by the MCP SDK may need to be discovered at runtime. Start with `mcp` and `mcp.server`, then check if additional loggers like `mcp.server.sse` or `mcp.server.transport` exist.
- Consider adding a custom filter that tags MCP protocol messages with `[PROTOCOL]` prefix for easy grep-ability.
- httpx logs at DEBUG level can be very verbose; may want to filter to only log request URLs and response status codes.

---

### T-006: Create MCP Tool Handler Classes

**Task ID**: T-006
**Task Name**: Create OOP tool handler classes for flight status, gate info, and weather
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase2-python-mcp-server.md](/docs/prps/phase2-python-mcp-server.md) -- Task 6

##### Feature Overview
Tool handlers are the business logic layer between MCP tool registration and HTTP clients. Each handler is an OOP class with an async `execute()` method that accepts tool parameters, calls the appropriate HTTP client, and formats the result as a string for MCP response.

##### Task Purpose
**As a** MCP tool function
**I need** tool handler classes that encapsulate parameter handling, client invocation, and response formatting
**So that** tool registration functions remain thin wrappers delegating to testable handler objects

##### Dependencies
- **Prerequisite Tasks**: T-002 (config), T-003 (models), T-004 (HTTP clients)
- **Parallel Tasks**: T-005 (protocol logger) -- no dependency
- **Integration Points**: HTTP clients (T-004), Config (T-002), Pydantic models (T-003)
- **Blocked By**: Nothing

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When `FlightStatusTool.execute(airport="BDL")` is called, it returns a formatted string with flight data
- **REQ-2**: When the HTTP client returns an empty list, the tool returns a "no results found" message
- **REQ-3**: When the HTTP client raises an error, the tool returns a user-friendly error message
- **REQ-4**: Each tool handler accepts its Config instance via constructor injection

##### Technical Constraints
- **Pattern**: OOP classes with base class `BaseTool` defining the `execute()` interface
- **Return type**: `str` (MCP tools return string content for display)
- **Error handling**: Catch httpx exceptions, return error message strings (do not re-raise into MCP protocol layer)

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp/src/tools/
├── __init__.py              - Re-export tool classes
├── base.py                  - BaseTool abstract base class
├── flight_status.py         - FlightStatusTool handler
├── gate_info.py             - GateInfoTool handler
└── weather.py               - WeatherTool handler
```

##### Key Implementation Steps
1. **Create `BaseTool`** abstract base class with `execute()` method signature -> Shared interface
2. **Create `FlightStatusTool`** with `execute(airport, flight_number, time)` -> Flight tool handler
3. **Create `GateInfoTool`** with `execute(airport, gate_number)` -> Gate tool handler
4. **Create `WeatherTool`** with `execute(airport)` -> Weather tool handler
5. **Implement response formatting** that converts Pydantic model lists to readable strings -> Human-readable output
6. **Add error handling** wrapping httpx exceptions into error message strings -> Graceful degradation

##### Code Patterns to Follow
```python
# tools/base.py pattern
from abc import ABC, abstractmethod
from src.config import Config

class BaseTool(ABC):
    """Base class for MCP tool handlers."""

    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Execute the tool and return a formatted string result."""
        ...

# tools/flight_status.py pattern
import logging
from src.tools.base import BaseTool
from src.clients.flight_status_client import FlightStatusClient
from src.config import Config
import httpx

logger = logging.getLogger(__name__)

class FlightStatusTool(BaseTool):
    """Handler for the get_flight_status MCP tool."""

    def __init__(self, config: Config):
        super().__init__(config)
        self.client = FlightStatusClient(config.flight_status_url)

    async def execute(
        self, airport: str = "", flight_number: str = "", time: str = ""
    ) -> str:
        try:
            flights = await self.client.get_flights(
                airport=airport, flight_number=flight_number, time=time
            )
            if not flights:
                return "No flights found matching the criteria."
            # Format each flight as a readable block
            results = []
            for f in flights:
                results.append(
                    f"Flight {f.flight_number} ({f.airline}): "
                    f"{f.origin} -> {f.destination}, "
                    f"Status: {f.status}, Gate: {f.gate}"
                )
            return "\n".join(results)
        except httpx.ConnectError:
            return "Error: Flight status service is unavailable."
        except httpx.TimeoutException:
            return "Error: Flight status service timed out."
        except httpx.HTTPStatusError as e:
            return f"Error: Flight status service returned {e.response.status_code}."
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Successful flight status query
  Given the flight-status HTTP client returns a list of Flight objects
  When FlightStatusTool.execute(airport="BDL") is called
  Then a formatted string with flight details is returned
  And the string contains flight numbers, airlines, and statuses

Scenario 2: No results found
  Given the HTTP client returns an empty list
  When any tool's execute() is called
  Then the return string contains "No ... found"

Scenario 3: Service unavailable
  Given the HTTP client raises httpx.ConnectError
  When any tool's execute() is called
  Then the return string starts with "Error:" and describes the issue

Scenario 4: Each tool uses Config for service URL
  Given a Config with custom service URLs
  When a tool handler is instantiated with that Config
  Then the tool's HTTP client uses the URL from Config
```

##### Rule-Based Criteria (Checklist)
- [ ] `BaseTool` abstract class with `execute()` method defined
- [ ] `FlightStatusTool` accepts `airport`, `flight_number`, `time` parameters
- [ ] `GateInfoTool` accepts `airport`, `gate_number` parameters
- [ ] `WeatherTool` accepts `airport` parameter
- [ ] All tools return `str` type
- [ ] Empty results produce a "no results" message, not an empty string
- [ ] httpx exceptions are caught and returned as error messages
- [ ] Config injected via constructor, not global state

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp
uv run ruff check src/tools/
```

##### Definition of Done
- [ ] All four tool files created (base + 3 tool handlers)
- [ ] Each tool delegates to its corresponding HTTP client
- [ ] Response formatting produces human-readable strings
- [ ] Error handling covers all httpx exception types
- [ ] Tools are re-exported from `src.tools.__init__`

---

### T-007: Create MCP Server Entry Point

**Task ID**: T-007
**Task Name**: Create MCP server entry point with FastMCP, tool registration, and SSE transport
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase2-python-mcp-server.md](/docs/prps/phase2-python-mcp-server.md) -- Task 7

##### Feature Overview
The server entry point is the central orchestration module. It initializes FastMCP, registers three tools using `@mcp.tool()` decorators, configures SSE transport, wires up protocol logging for debug mode, and parses CLI arguments.

##### Task Purpose
**As a** system operator
**I need** a server entry point that starts the MCP server with all tools registered
**So that** MCP clients can discover and invoke aviation tools over SSE transport

##### Dependencies
- **Prerequisite Tasks**: T-002 (config), T-005 (protocol logger), T-006 (tool handlers)
- **Parallel Tasks**: None -- this is the integration point for all prior work
- **Integration Points**: FastMCP server API, SSE transport, all tool handlers
- **Blocked By**: Nothing

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When the server starts, it initializes FastMCP with name "aviation-mcp"
- **REQ-2**: When the server starts, three tools are registered: `get_flight_status`, `get_gate_info`, `get_weather`
- **REQ-3**: When `--debug` flag is passed, protocol-level logging is enabled
- **REQ-4**: When an MCP client connects via SSE, it can discover and invoke all three tools
- **REQ-5**: The server listens on port 8000 with SSE transport

##### Non-Functional Requirements
- **Performance**: Server starts within 5 seconds
- **Compatibility**: SSE transport (GET `/sse`, POST `/messages`)

##### Technical Constraints
- **Library**: `mcp.server.fastmcp.FastMCP`
- **Transport**: SSE via `mcp.run(transport="sse")`
- **Port**: 8000 (default FastMCP SSE port, or configure explicitly)
- **Binding**: `0.0.0.0` for Docker compatibility

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp/src/server.py    - MCP server entry point
```

##### Key Implementation Steps
1. **Initialize FastMCP** with server name "aviation-mcp" -> Server instance
2. **Register three tools** using `@mcp.tool()` decorator on async functions -> Tool discovery
3. **Each tool function** instantiates its handler class, calls `execute()`, returns result -> Thin wrapper pattern
4. **Parse `--debug` CLI argument** using `argparse` -> Debug mode control
5. **Call `setup_protocol_logging()`** if debug mode -> Protocol logging activation
6. **Start server** with `mcp.run(transport="sse")` -> SSE listener on port 8000

##### Code Patterns to Follow
```python
# server.py pattern (from PRP pseudocode)
import argparse
from mcp.server.fastmcp import FastMCP
from src.tools.flight_status import FlightStatusTool
from src.tools.gate_info import GateInfoTool
from src.tools.weather import WeatherTool
from src.logging.protocol_logger import setup_protocol_logging
from src.config import Config

mcp_server = FastMCP("aviation-mcp")
config = Config()

@mcp_server.tool()
async def get_flight_status(
    airport: str = "", flight_number: str = "", time: str = ""
) -> str:
    """Get flight status information for an airport.

    Args:
        airport: IATA airport code (e.g., BDL, JFK)
        flight_number: Flight number (e.g., 1234)
        time: Departure time filter (ISO 8601 prefix)
    """
    tool = FlightStatusTool(config)
    return await tool.execute(airport=airport, flight_number=flight_number, time=time)

@mcp_server.tool()
async def get_gate_info(airport: str = "", gate_number: str = "") -> str:
    """Get gate information for an airport.

    Args:
        airport: IATA airport code (e.g., BDL, JFK)
        gate_number: Gate identifier (e.g., A1, B12)
    """
    tool = GateInfoTool(config)
    return await tool.execute(airport=airport, gate_number=gate_number)

@mcp_server.tool()
async def get_weather(airport: str = "") -> str:
    """Get current weather conditions for an airport.

    Args:
        airport: IATA airport code (e.g., BDL, JFK)
    """
    tool = WeatherTool(config)
    return await tool.execute(airport=airport)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aviation MCP Server")
    parser.add_argument("--debug", action="store_true", help="Enable protocol debug logging")
    args = parser.parse_args()

    if args.debug or config.debug:
        setup_protocol_logging()

    mcp_server.run(transport="sse")
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Server starts successfully
  Given all dependencies are installed and config is valid
  When "uv run src/server.py" is executed
  Then the server starts listening on port 8000 for SSE connections
  And no errors are printed to stderr

Scenario 2: Tools are discoverable
  Given the server is running
  When an MCP client connects and requests tool listing
  Then three tools are returned: get_flight_status, get_gate_info, get_weather
  And each tool has parameter descriptions from docstrings

Scenario 3: Tool invocation works
  Given the server is running and C# services are available
  When an MCP client invokes get_flight_status with airport="BDL"
  Then the tool returns formatted flight data as a string

Scenario 4: Debug mode activates logging
  Given the server is started with "--debug" flag
  When an MCP client connects
  Then protocol-level log messages appear in stderr
  And JSON-RPC message details are visible

Scenario 5: Debug mode via environment variable
  Given MCP_DEBUG=true is set in the environment
  When the server starts without --debug flag
  Then protocol-level logging is still enabled
```

##### Rule-Based Criteria (Checklist)
- [ ] FastMCP initialized with name "aviation-mcp"
- [ ] Three tools registered with correct names and parameter signatures
- [ ] Tool docstrings provide clear descriptions for MCP clients
- [ ] `--debug` CLI flag parsed and triggers protocol logging
- [ ] `MCP_DEBUG` env var also triggers protocol logging
- [ ] SSE transport configured
- [ ] Server binds to `0.0.0.0` for Docker compatibility
- [ ] Tool functions are thin wrappers delegating to handler classes

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp
uv run ruff check src/server.py

# Start server (verify no startup errors)
uv run src/server.py --debug &
sleep 2
curl -s http://localhost:8000/sse -H "Accept: text/event-stream" | head -5
kill %1
```

##### Definition of Done
- [ ] `server.py` created and runnable
- [ ] Three tools registered and discoverable
- [ ] Debug mode works via both CLI flag and env var
- [ ] SSE transport starts on port 8000
- [ ] Tool invocation delegates to handler classes
- [ ] MCP Inspector can connect and list tools

#### Resources & References

##### Documentation Links
- **MCP SDK FastMCP**: https://modelcontextprotocol.github.io/python-sdk/ -- Server setup, tool registration
- **MCP Inspector**: `npx -y @modelcontextprotocol/inspector` -- Manual testing tool

##### Implementation Notes
- The variable name for the FastMCP instance should avoid shadowing the `mcp` package import. Use `mcp_server` or `server` instead of `mcp`.
- `mcp.run(transport="sse")` defaults to port 8000. If explicit port configuration is needed, check FastMCP constructor or `run()` parameters.
- Tool function docstrings are used by the MCP SDK to generate tool descriptions sent to clients -- make them clear and informative.

---

### T-008: Create Pytest Test Suite

**Task ID**: T-008
**Task Name**: Create pytest tests for HTTP clients and tool handlers with mocked HTTP responses
**Priority**: High

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase2-python-mcp-server.md](/docs/prps/phase2-python-mcp-server.md) -- Task 8

##### Feature Overview
Comprehensive pytest test suite covering the HTTP client layer (mocked HTTP responses) and tool handler layer (mocked clients). Tests verify correct parameter passing, response parsing, error handling, and output formatting.

##### Task Purpose
**As a** developer
**I need** automated tests for all HTTP clients and tool handlers
**So that** I can verify correctness and catch regressions without running the full service stack

##### Dependencies
- **Prerequisite Tasks**: T-004 (HTTP clients), T-006 (tool handlers)
- **Parallel Tasks**: T-009 (Dockerfile) -- no dependency
- **Integration Points**: pytest, pytest-asyncio, pytest-httpx
- **Blocked By**: Nothing

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When `uv run pytest` is executed, all tests pass
- **REQ-2**: HTTP client tests use `pytest-httpx` to mock HTTP responses without hitting real services
- **REQ-3**: Tool handler tests verify response formatting and error handling
- **REQ-4**: Tests cover happy path, empty results, and error conditions

##### Technical Constraints
- **Libraries**: `pytest`, `pytest-asyncio` (for async test functions), `pytest-httpx` (for httpx mocking)
- **Pattern**: `conftest.py` with shared fixtures; separate test directories for clients and tools
- **Async mode**: `asyncio_mode = "auto"` in `pyproject.toml` for automatic async test detection

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp/tests/
├── __init__.py
├── conftest.py                          - Shared fixtures (sample data, config)
├── test_clients/
│   ├── __init__.py
│   ├── test_flight_status_client.py     - FlightStatusClient tests
│   ├── test_gate_info_client.py         - GateInfoClient tests
│   └── test_weather_client.py           - WeatherClient tests
└── test_tools/
    ├── __init__.py
    ├── test_flight_status.py            - FlightStatusTool tests
    ├── test_gate_info.py                - GateInfoTool tests
    └── test_weather.py                  - WeatherTool tests
```

##### Key Implementation Steps
1. **Create `conftest.py`** with shared fixtures: sample JSON data, Config instances, mock responses -> Test infrastructure
2. **Create client tests** using `pytest-httpx` `httpx_mock` fixture to mock HTTP GET responses -> Client layer verification
3. **Create tool handler tests** that mock HTTP client responses and verify output formatting -> Handler layer verification
4. **Test error scenarios** (connection error, timeout, non-200 status) -> Error handling verification
5. **Test empty results** to verify "no results" messaging -> Edge case coverage

##### Code Patterns to Follow
```python
# tests/conftest.py pattern
import pytest
from src.config import Config

@pytest.fixture
def config():
    """Config with localhost URLs for testing."""
    return Config()

@pytest.fixture
def sample_flight_data():
    """Sample flight JSON matching C# service response."""
    return [
        {
            "airport": "BDL",
            "flightNumber": "1234",
            "airline": "Delta",
            "origin": "BDL",
            "destination": "JFK",
            "departureTime": "2026-02-09T08:00:00",
            "arrivalTime": "2026-02-09T10:00:00",
            "status": "On Time",
            "gate": "A1",
            "terminal": "A",
        }
    ]

@pytest.fixture
def sample_gate_data():
    return [
        {
            "airport": "BDL",
            "gateNumber": "A1",
            "terminal": "A",
            "status": "Occupied",
            "assignedFlight": "DL1234",
            "airline": "Delta",
            "lastUpdated": "2026-02-09T08:00:00",
        }
    ]

@pytest.fixture
def sample_weather_data():
    return [
        {
            "airport": "BDL",
            "condition": "Partly Cloudy",
            "temperatureF": 45.0,
            "temperatureC": 7.2,
            "windSpeed": "15 mph NW",
            "visibility": "10 miles",
            "humidity": 55,
            "lastUpdated": "2026-02-09T08:00:00",
        }
    ]

# tests/test_clients/test_flight_status_client.py pattern
import pytest
from src.clients.flight_status_client import FlightStatusClient

@pytest.mark.asyncio
async def test_get_flights_success(httpx_mock, sample_flight_data):
    httpx_mock.add_response(json=sample_flight_data)
    client = FlightStatusClient("http://localhost:5001")
    flights = await client.get_flights(airport="BDL")
    assert len(flights) == 1
    assert flights[0].flight_number == "1234"
    assert flights[0].airport == "BDL"

@pytest.mark.asyncio
async def test_get_flights_empty(httpx_mock):
    httpx_mock.add_response(json=[])
    client = FlightStatusClient("http://localhost:5001")
    flights = await client.get_flights(airport="UNKNOWN")
    assert flights == []

@pytest.mark.asyncio
async def test_get_flights_filters_empty_params(httpx_mock, sample_flight_data):
    httpx_mock.add_response(json=sample_flight_data)
    client = FlightStatusClient("http://localhost:5001")
    await client.get_flights(airport="BDL", flight_number="", time="")
    request = httpx_mock.get_request()
    assert "flightNumber" not in str(request.url)

# tests/test_tools/test_flight_status.py pattern
import pytest
from unittest.mock import AsyncMock, patch
from src.tools.flight_status import FlightStatusTool
from src.models.flight import Flight

@pytest.mark.asyncio
async def test_execute_returns_formatted_string(config):
    tool = FlightStatusTool(config)
    mock_flights = [
        Flight(
            airport="BDL", flight_number="1234", airline="Delta",
            origin="BDL", destination="JFK",
            departure_time="2026-02-09T08:00:00",
            arrival_time="2026-02-09T10:00:00",
            status="On Time", gate="A1", terminal="A",
        )
    ]
    with patch.object(tool.client, "get_flights", new_callable=AsyncMock, return_value=mock_flights):
        result = await tool.execute(airport="BDL")
    assert "1234" in result
    assert "Delta" in result
    assert "On Time" in result

@pytest.mark.asyncio
async def test_execute_no_results(config):
    tool = FlightStatusTool(config)
    with patch.object(tool.client, "get_flights", new_callable=AsyncMock, return_value=[]):
        result = await tool.execute(airport="UNKNOWN")
    assert "No" in result.lower() or "no" in result.lower()
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: All tests pass
  Given the test suite is complete
  When "uv run pytest tests/ -v" is executed
  Then all tests pass with no failures

Scenario 2: Client tests mock HTTP correctly
  Given httpx_mock is configured with sample data
  When a client method is called
  Then it returns parsed Pydantic models without hitting a real server

Scenario 3: Tool tests verify error handling
  Given a client method is mocked to raise httpx.ConnectError
  When the tool's execute() is called
  Then the returned string contains "Error"

Scenario 4: Tests cover all three services
  Given the test suite
  When test files are counted
  Then there are 3 client test files and 3 tool test files
```

##### Rule-Based Criteria (Checklist)
- [ ] `conftest.py` with sample data fixtures for all three services
- [ ] Client tests: happy path, empty results, parameter filtering for each service
- [ ] Tool tests: happy path, empty results, error handling for each service
- [ ] All tests are async (use `@pytest.mark.asyncio` or auto mode)
- [ ] `uv run pytest` passes with 0 failures
- [ ] Tests do not require running C# services (fully mocked)

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp
uv run ruff check tests/
uv run pytest tests/ -v --tb=short
```

##### Definition of Done
- [ ] All test files created per the directory structure
- [ ] `conftest.py` provides shared fixtures
- [ ] Client layer fully tested with mocked HTTP
- [ ] Tool handler layer fully tested with mocked clients
- [ ] Error scenarios covered
- [ ] `uv run pytest` passes

---

### T-009: Create Dockerfile

**Task ID**: T-009
**Task Name**: Create Dockerfile for the Python MCP server
**Priority**: High

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase2-python-mcp-server.md](/docs/prps/phase2-python-mcp-server.md) -- Task 9

##### Feature Overview
Docker packaging for the MCP server, enabling it to run alongside the Phase 1 C# services on a shared Docker network. The container must expose port 8000 for SSE connections and resolve C# service hostnames via Docker DNS.

##### Task Purpose
**As a** system operator
**I need** a Docker image for the MCP server
**So that** the server can run in Docker Compose alongside C# services with proper networking

##### Dependencies
- **Prerequisite Tasks**: T-001 (project structure), T-007 (server entry point)
- **Parallel Tasks**: T-008 (tests) -- no dependency
- **Integration Points**: Docker Compose (Phase 3), C# service containers
- **Blocked By**: Nothing

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When `docker build` is run, the image builds without errors
- **REQ-2**: When the container starts, the MCP server listens on port 8000
- **REQ-3**: When running on a Docker network with C# services, the server can reach them by hostname

##### Non-Functional Requirements
- **Performance**: Image should be reasonably small (use `python:3.13-slim`)
- **Security**: Non-root user execution preferred
- **Build time**: Use layer caching (copy `pyproject.toml` before source code)

##### Technical Constraints
- **Base image**: `python:3.13-slim`
- **Package manager**: `uv` (install in image)
- **Port**: 8000 exposed
- **Binding**: `0.0.0.0` (not localhost) for Docker port mapping

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp/Dockerfile    - Multi-stage or single-stage Docker build
```

##### Key Implementation Steps
1. **Start from `python:3.13-slim`** base image -> Minimal Python runtime
2. **Install `uv`** via pip or curl -> Package manager available in container
3. **Copy `pyproject.toml` and `uv.lock`** first -> Layer caching for dependencies
4. **Run `uv sync`** to install dependencies -> Dependencies cached
5. **Copy source code** -> Application files in container
6. **Expose port 8000** -> SSE transport port
7. **Set entrypoint** to `uv run src/server.py` -> Server starts on container launch

##### Code Patterns to Follow
```dockerfile
# Dockerfile pattern
FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files first (layer caching)
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY src/ src/

# Expose MCP SSE port
EXPOSE 8000

# Start MCP server
ENTRYPOINT ["uv", "run", "src/server.py"]
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Docker image builds successfully
  Given the Dockerfile and source code are present
  When "docker build -t aviation-mcp ." is run from src/aviation-mcp/
  Then the image builds without errors
  And the image size is under 500MB

Scenario 2: Container starts and listens
  Given the Docker image is built
  When "docker run -p 8000:8000 aviation-mcp" is executed
  Then the MCP server starts listening on port 8000
  And curl to http://localhost:8000/sse returns an SSE connection

Scenario 3: Container reaches C# services on Docker network
  Given a Docker network with C# services running
  When the MCP server container starts on the same network
  Then it can resolve hostname "flight-status" to the C# service container
  And tool invocations successfully reach the C# services
```

##### Rule-Based Criteria (Checklist)
- [ ] Dockerfile exists at `src/aviation-mcp/Dockerfile`
- [ ] Base image is `python:3.13-slim`
- [ ] `uv` installed in the image
- [ ] Dependencies installed via `uv sync` with layer caching
- [ ] Source code copied after dependencies (build cache optimization)
- [ ] Port 8000 exposed
- [ ] Entrypoint runs the MCP server
- [ ] Image builds without errors
- [ ] Container starts and server listens on port 8000

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp
docker build -t aviation-mcp .
docker run --rm -p 8000:8000 aviation-mcp &
sleep 3
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/sse
docker stop $(docker ps -q --filter ancestor=aviation-mcp)
```

##### Definition of Done
- [ ] Dockerfile created
- [ ] Image builds successfully
- [ ] Container starts and server listens on port 8000
- [ ] Layer caching optimized (dependencies before source)

#### Resources & References

##### Documentation Links
- **uv Docker guide**: https://docs.astral.sh/uv/guides/integration/docker/ -- uv in Docker containers
- **Python Docker best practices**: https://docs.docker.com/language/python/ -- Slim images, layer caching

##### Implementation Notes
- If `uv.lock` does not exist yet (first build), the `COPY pyproject.toml uv.lock* ./` pattern with the glob safely handles the missing file.
- Consider adding `--no-dev` to `uv sync` in the Dockerfile to exclude test dependencies from the production image.
- The server must bind to `0.0.0.0`, not `127.0.0.1`, for Docker port mapping to work. Verify that FastMCP's `run(transport="sse")` uses `0.0.0.0` by default or configure it explicitly.

---

## Implementation Recommendations

### Suggested Team Structure
This is a single-developer project, but the work breaks down into clear skill areas:
- **Python backend**: All 9 tasks (one developer, sequential with some parallelism)
- **DevOps/Docker**: T-009 can be done by someone with Docker experience

### Optimal Task Sequencing

```
Phase 1 (Foundation):
  T-001 ──> T-002 ──┐
            T-003 ──┤ (T-002 and T-003 can be parallel)
                    │
Phase 2 (Core):     v
            T-004 ──┐
            T-005 ──┤ (T-004 and T-005 can be parallel)
                    │
            T-006 ──┤ (depends on T-004, T-002, T-003)
                    │
            T-007 ──┤ (depends on T-006, T-005, T-002)
                    │
Phase 3 (Quality):  v
            T-008 ──┐ (depends on T-004, T-006)
            T-009 ──┘ (depends on T-007; parallel with T-008)
```

### Parallelization Opportunities
1. **T-002 and T-003** (config and models) have no dependency on each other
2. **T-004 and T-005** (HTTP clients and protocol logger) have no dependency on each other
3. **T-008 and T-009** (tests and Dockerfile) have no dependency on each other

### Resource Allocation Suggestions
- Allocate the most time to T-004 (HTTP clients) and T-006 (tool handlers) as they have the most business logic
- T-007 (server entry point) is the integration point -- budget time for debugging SSE transport issues
- T-008 (tests) will take significant time due to async mocking complexity
- T-001 (project setup) and T-009 (Dockerfile) are the fastest tasks

---

## Critical Path Analysis

### Tasks on Critical Path
```
T-001 -> T-003 -> T-004 -> T-006 -> T-007 -> T-008
```

The critical path runs through the core data flow: project setup, models, HTTP clients, tool handlers, server integration, and tests. Each step depends on the previous.

### Potential Bottlenecks
1. **T-004 (HTTP clients)**: camelCase/snake_case mapping and async error handling may need iteration
2. **T-007 (server entry point)**: First time the full stack is wired together; SSE transport issues may surface
3. **T-008 (tests)**: Async test fixtures and httpx mocking can be tricky to get right

### Schedule Optimization Suggestions
- Start T-002 and T-003 in parallel immediately after T-001
- Start T-005 as soon as T-001 is done (does not need models or config)
- Start T-009 as soon as T-007 is done (does not need tests)
- Run manual MCP Inspector verification after T-007 before investing in T-008

---

## Anti-Patterns to Avoid (from PRP)

- **Do not** use `requests` library (synchronous) -- use `httpx` for async compatibility
- **Do not** hardcode service URLs -- use environment variables for Docker networking
- **Do not** catch all exceptions in tool handlers -- let MCP SDK handle protocol-level errors
- **Do not** mix sync and async patterns -- the MCP server is fully async
- **Do not** shadow the `mcp` package import with the FastMCP instance variable name
