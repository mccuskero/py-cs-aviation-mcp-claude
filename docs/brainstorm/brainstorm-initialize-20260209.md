# Feature Brainstorming Session: Aviation MCP — Project Initialization

**Date:** 2026-02-09
**Session Type:** Feature Planning / Technical Design

## 1. Context & Problem Statement

### Problem Description
There is a need to demonstrate a clean architectural pattern for connecting AI agents to backend microservices using the Model Context Protocol (MCP). The project showcases a Python MCP server acting as an intermediary between AI agents and three C# microservices serving aviation data (flight status, gate info, weather). The emphasis is on making the pattern visible, understandable, and reproducible.

### Target Users
- **Primary Users:** Developers and architects looking to understand how to wire an MCP server to backend microservices across language boundaries (Python ↔ C#).
- **Secondary Users:** Teams evaluating MCP as a protocol for connecting AI agents to enterprise services.

### Success Criteria
- **Architecture Clarity:** A developer can follow the request flow from CLI client → MCP server → C# service and back by reading the code and debug logs.
- **Protocol Visibility:** Protocol-level debug mode exposes JSON-RPC messages, tool registration, and capability negotiation.
- **Independent Deployability:** Each C# microservice runs independently in its own Docker container with its own Swagger UI.
- **Test Coverage:** All three testing levels pass — unit (C# xUnit, Python pytest), and integration (docker-compose + CLI client).

### Constraints & Assumptions
- **Technical Constraints:**
  - Python 3.13 for MCP server; .NET 8 for C# microservices
  - `uv` for Python package management
  - Docker Compose for orchestration
  - Microservices return stubbed (parameterized) data from JSON files — no real aviation data sources
- **Assumptions Made:**
  - The MCP protocol and SDK are stable enough for demonstration purposes
  - LangChain v1.2.6+ supports MCP client integration for the CLI test client
  - A small dataset (handful of airports, flights, gates) is sufficient to demonstrate parameterized behavior

## 2. Brainstormed Ideas & Options

### Option A: Monolithic MCP Server with Embedded Logic
- **Description:** Build the MCP server with stubbed aviation logic directly embedded — no separate C# services.
- **Pros:**
  - Simplest to build and deploy
  - No cross-language complexity
- **Cons:**
  - Fails to demonstrate cross-language service communication
  - No microservice architecture to showcase
  - Doesn't reflect real-world patterns
- **Effort Estimate:** S
- **Risk Level:** Low
- **Dependencies:** None

### Option B: Python MCP Server + C# Microservices (Selected)
- **Description:** Python MCP server (official `mcp` SDK) calls three independent C# microservices over REST. Each microservice follows a layered Controller → Service → Core pattern. LangChain powers a separate CLI test client. Protocol-level debug logging traces the full request lifecycle.
- **Key Features:**
  - MCP server exposes three tools: flight-status, gate-info, weather
  - Protocol-level debug logging (JSON-RPC messages, tool registration, capability negotiation)
  - Parameterized C# stubs with JSON data filtering
  - Swagger UI per microservice
  - Docker Compose orchestrates everything
  - Three-tier testing: xUnit, pytest, integration
- **Pros:**
  - Demonstrates all three focus areas (MCP mechanics, cross-lang comms, microservice structure)
  - Clean separation of concerns — each framework does what it's best at
  - Independently deployable services
  - Protocol debug mode makes the pattern tangible
- **Cons:**
  - More complex initial setup (Docker, two languages, multiple projects)
  - Requires familiarity with both Python and C# ecosystems
- **Effort Estimate:** L
- **Risk Level:** Medium
- **Dependencies:** MCP Python SDK, LangChain, .NET 8 SDK, Docker

### Option C: Python MCP Server + Python Microservices
- **Description:** Same architecture but with Python (FastAPI) microservices instead of C#.
- **Pros:**
  - Single language simplifies development
  - Faster to build
- **Cons:**
  - Doesn't demonstrate cross-language communication
  - Less representative of enterprise environments where polyglot is common
- **Effort Estimate:** M
- **Risk Level:** Low
- **Dependencies:** FastAPI, MCP Python SDK

## 3. Decision Outcome

### Chosen Approach
**Selected Solution:** Option B — Python MCP Server + C# Microservices

### Rationale
**Primary Factors in Decision:**
- **Cross-language demonstration is core to the value:** The Python ↔ C# boundary is the most interesting part of the architecture and the hardest to find examples of.
- **Enterprise relevance:** Many organizations run polyglot stacks; this pattern is directly applicable.
- **MCP protocol visibility:** Using the official MCP SDK with protocol-level debug logging makes the pattern educational, not just functional.
- **Framework alignment:** MCP SDK for the server (protocol-native) and LangChain for the client (agent-native) shows each tool in its ideal role.

### Trade-offs Accepted
- **What We're Gaining:** Full demonstration of MCP ↔ REST microservice pattern across languages with protocol visibility.
- **What We're Sacrificing:** Speed of initial development; maintaining two language ecosystems.
- **Future Considerations:** The C# services could be swapped for real aviation APIs later without changing the MCP server interface.

## 4. Implementation Plan

### MVP Scope (Phase 1): Stubbed C# Microservices
**Core Features for Initial Release:**
- [ ] Flight-status microservice: .NET 8, Controller pattern, Swagger, parameterized JSON stubs
  - Endpoint: `GET /api/flights?airport={code}&flightNumber={number}&time={time}`
  - Returns filtered flight data or 404
- [ ] Gate-info microservice: same pattern
  - Endpoint: `GET /api/gates?airport={code}&gateNumber={number}`
  - Returns filtered gate data or 404
- [ ] Weather microservice: same pattern
  - Endpoint: `GET /api/weather?airport={code}`
  - Returns weather data for airport or 404
- [ ] Each service has: CLI project, Core (models), Services (business logic), Tests (xUnit)
- [ ] Dockerfiles for each microservice
- [ ] JSON data files with parameterized test data (3-5 airports)

**C# Project Structure (per service):**
```
flight-status/
├── Dockerfile
└── src/
    ├── FLIGHTSTATUS.CLI/          # ASP.NET Core entry point, Program.cs, Swagger config
    ├── FLIGHTSTATUS.Core/         # Models, DTOs, interfaces
    ├── FLIGHTSTATUS.Services/     # Business logic, JSON data loading, filtering
    └── FLIGHTSTATUS.Tests/        # xUnit tests for service + controller layers
```

**Acceptance Criteria:**
- Each microservice starts independently and serves Swagger UI
- Parameterized queries return correct filtered results from JSON data
- Unknown parameters return appropriate HTTP 404 responses
- xUnit tests pass for service layer (data filtering) and controller layer (HTTP responses)

### MVP Scope (Phase 2): Python MCP Server
- [ ] MCP server using official `mcp` Python SDK
- [ ] Three MCP tools registered: `get_flight_status`, `get_gate_info`, `get_weather`
- [ ] Each tool calls the corresponding C# microservice via HTTP REST
- [ ] Protocol-level debug logging mode showing:
  - JSON-RPC message framing
  - Tool registration and capability negotiation
  - Request/response flow to C# services
- [ ] Object-oriented design (tool handlers as classes)
- [ ] Dockerfile for the MCP server
- [ ] pytest unit tests for tool handlers and HTTP client layer

**Python Project Structure:**
```
aviation-mcp/
├── Dockerfile
├── pyproject.toml
└── src/
    ├── server.py                  # MCP server entry point, tool registration
    ├── tools/                     # Tool handler classes
    │   ├── flight_status.py
    │   ├── gate_info.py
    │   └── weather.py
    ├── clients/                   # HTTP clients for C# services
    │   ├── flight_status_client.py
    │   ├── gate_info_client.py
    │   └── weather_client.py
    ├── models/                    # Data models
    └── logging/                   # Debug/protocol logging
        └── protocol_logger.py
```

### MVP Scope (Phase 3): CLI Test Client
- [ ] LangChain-based CLI client that connects to the MCP server
- [ ] Exercises all three tools with sample queries
- [ ] Displays results and can trigger debug mode on the server
- [ ] docker-compose.yml orchestrating all services + MCP server

**Acceptance Criteria:**
- `docker-compose up` starts all four services
- CLI client can query flight status, gate info, and weather through the MCP server
- Debug mode shows full protocol-level trace from client request to C# response

### Future Enhancements (Phase 2+)
- Swap stubbed JSON data for real aviation API integrations
- Add authentication/authorization layer to the MCP server
- Add streaming responses for real-time flight tracking
- Add a web-based UI client in addition to CLI

## 5. Action Items & Next Steps

### Immediate Actions (This Week)
- [ ] **Create the C# flight-status microservice**
  - **Dependencies:** .NET 8 SDK, project scaffolding
  - **Success Criteria:** Service starts, Swagger UI accessible, parameterized queries work, xUnit tests pass

- [ ] **Create the C# gate-info microservice**
  - **Dependencies:** Same as flight-status; can follow same pattern
  - **Success Criteria:** Same as flight-status

- [ ] **Create the C# weather microservice**
  - **Dependencies:** Same as above
  - **Success Criteria:** Same as flight-status

- [ ] **Create Dockerfiles for all three C# services**
  - **Dependencies:** Working microservices
  - **Success Criteria:** `docker build` and `docker run` work for each

### Short-term Actions (Next Sprint)
- [ ] **Build the Python MCP server with protocol debug logging**
- [ ] **Build the LangChain CLI test client**
- [ ] **Create docker-compose.yml for full stack orchestration**
- [ ] **Write pytest tests for MCP server tool handlers and HTTP clients**
- [ ] **End-to-end integration test via docker-compose + CLI client**

## 6. Risks & Dependencies

### Technical Risks
- **Risk:** MCP Python SDK may have breaking changes or incomplete protocol-level logging hooks
  - **Impact:** High
  - **Probability:** Medium
  - **Mitigation Strategy:** Pin SDK version; implement custom protocol logger wrapping the SDK's transport layer

- **Risk:** LangChain MCP client integration may require specific version compatibility
  - **Impact:** Medium
  - **Probability:** Medium
  - **Mitigation Strategy:** Verify LangChain + MCP SDK compatibility early; pin versions in pyproject.toml

- **Risk:** Docker networking between Python and C# containers
  - **Impact:** Medium
  - **Probability:** Low
  - **Mitigation Strategy:** Use docker-compose service names for DNS resolution; test connectivity early

- **Risk:** JSON stub data may not cover enough edge cases for meaningful parameterized queries
  - **Impact:** Low
  - **Probability:** Low
  - **Mitigation Strategy:** Design JSON data files with 3-5 airports, multiple flights per airport, varied gate statuses, and different weather conditions

## 7. Resources & References

### Technical Documentation
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — Server implementation, tool registration, transport
- [MCP Specification](https://spec.modelcontextprotocol.io/) — Protocol details, JSON-RPC framing, capability negotiation
- [LangChain MCP Integration](https://python.langchain.com/) — Client-side MCP tool usage
- [ASP.NET Core .NET 8 Controllers](https://learn.microsoft.com/en-us/aspnet/core/) — Controller pattern, Swagger/Swashbuckle setup
- [uv Package Manager](https://docs.astral.sh/uv/) — Python dependency management

### Codebase References
- `src/flight-status/src/FLIGHTSTATUS.Services/` — Service layer pattern to replicate across gate-info and weather
- `src/aviation-mcp/src/tools/` — Tool handler pattern for MCP server
- `src/aviation-mcp/src/logging/protocol_logger.py` — Protocol-level debug logging implementation

## 8. Session Notes & Insights

### Key Insights Discovered
- **Framework separation strengthens the demo:** Using MCP SDK for the server and LangChain for the client shows each tool in its ideal role rather than forcing one framework to do everything.
- **Protocol-level debug logging is the differentiator:** Most MCP examples show the happy path. Exposing JSON-RPC messages, tool registration, and capability negotiation makes this project educational.
- **Parameterized stubs hit the sweet spot:** They're complex enough to demonstrate real service contracts (filtering, 404s) without the overhead of real data sources.
- **Controller pattern over Minimal APIs:** Even though the services are small, the Controller → Service → Core layering shows enterprise microservice structure clearly.

### Questions Raised (For Future Investigation)
- What specific version of the MCP Python SDK to pin for stability?
- What LangChain version provides the best MCP client support?
- Should the JSON stub data include temporal data (e.g., flights at different times) or keep time handling simple?
- How to best structure protocol-level logging — wrap the MCP SDK transport or use middleware?

### Decisions Log
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Project purpose | Architectural pattern demonstration | Prioritize clarity over production hardening |
| Focus areas | MCP protocol, cross-lang comms, microservice structure | Three pillars of the pattern |
| MCP server framework | Official `mcp` Python SDK | Protocol-native, supports debug logging |
| CLI client framework | LangChain v1.2.6+ | Agent-native, ideal for client/tool orchestration |
| C# API style | Controllers (not Minimal APIs) | Shows enterprise layered structure |
| .NET version | .NET 8 (LTS) | Current LTS, Swagger support |
| Stub approach | Parameterized JSON stubs | Demonstrates real contracts without external dependencies |
| Debug logging | Protocol-level in debug mode | Shows JSON-RPC framing, tool registration, capability negotiation |
| Testing strategy | xUnit + pytest + docker-compose integration | Full coverage across all layers |
