# Phase 3: CLI Test Client & Docker Compose Orchestration -- Task Breakdown

> **Source PRP**: [docs/prps/phase3-cli-test-client.md](/Users/owenmccusker/Documents/dev/claude/py-cs-aviation-mcp-claude/docs/prps/phase3-cli-test-client.md)
> **Generated**: 2026-02-09
> **Template**: [docs/templates/technical-task-template.md](/Users/owenmccusker/Documents/dev/claude/py-cs-aviation-mcp-claude/docs/templates/technical-task-template.md)

---

## PRP Analysis Summary

- **Feature Name**: CLI Test Client & Docker Compose Orchestration (Phase 3 of 3)
- **Scope**: LangChain-based CLI client with interactive REPL and batch test modes, plus docker-compose.yml to orchestrate all services (3 C# microservices + Python MCP server)
- **Key Technical Requirements**:
  - LangChain v1.2.6+ with `langchain-mcp-adapters` for MCP SSE connection
  - `MultiServerMCPClient` for agent mode, `mcp.client.sse.sse_client` for batch mode (no LLM needed)
  - `create_react_agent` from LangGraph for interactive agent loop
  - Docker Compose with health checks and `depends_on: condition: service_healthy`
  - Two client modes: interactive REPL (requires LLM API key) and batch test (LLM-free, direct tool calls)
- **Validation Requirements**:
  - All batch test scenarios pass (exit code 0)
  - Interactive mode routes natural language queries to correct MCP tools
  - `docker-compose up --build` starts all 4 services with proper health check ordering
  - Debug logs show full protocol trace during client interaction
  - pytest tests pass for client module

## Task Complexity Assessment

- **Overall Complexity**: Moderate
- **Rationale**: Well-established patterns (LangChain agent, docker-compose), but integration with MCP SSE transport via `langchain-mcp-adapters` introduces version compatibility risk. The async REPL loop with blocking `input()` requires careful handling.
- **Integration Points**:
  - CLI client to MCP server via SSE (port 8000)
  - MCP server to 3 C# microservices (ports 5001, 5002, 5003)
  - Docker networking (aviation-net bridge network)
  - LLM provider API (interactive mode only)
- **Technical Challenges**:
  - `langchain-mcp-adapters` SSE support may have version compatibility issues
  - `MultiServerMCPClient` is an async context manager -- cannot reuse outside context
  - Batch mode must bypass LLM entirely (direct MCP tool calls via `ClientSession`)
  - Blocking `input()` in async REPL loop requires `asyncio.to_thread` or similar
  - Docker health check timing -- C# services must be fully ready before MCP server starts

## Phase Organization

This feature is organized into **3 logical phases** with 8 total tasks:

### Phase A: Infrastructure & Foundation (Tasks 1-3)
- **Objective**: Docker orchestration and client project scaffolding
- **Deliverables**: docker-compose.yml, pyproject.toml, config module
- **Milestone**: `docker-compose config` validates; `uv sync` installs all dependencies

### Phase B: Core Client Implementation (Tasks 4-6)
- **Objective**: LangChain agent, batch test runner, and CLI entry point
- **Deliverables**: agent.py, test_runner.py, client.py
- **Milestone**: Batch tests pass against running MCP server; interactive REPL functional

### Phase C: Testing & Integration (Tasks 7-8)
- **Objective**: pytest unit tests and full end-to-end integration validation
- **Deliverables**: test_client.py, validated docker-compose stack
- **Milestone**: `uv run pytest` passes; `docker-compose up --build` + batch test = exit code 0

---

## Detailed Task Breakdown

---

### T-301: Create docker-compose.yml for Full Stack Orchestration

**Task ID**: T-301
**Task Name**: Create docker-compose.yml for Full Stack Orchestration
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase3-cli-test-client.md](/Users/owenmccusker/Documents/dev/claude/py-cs-aviation-mcp-claude/docs/prps/phase3-cli-test-client.md) -- Task 1

##### Feature Overview
The docker-compose.yml is the single orchestration file that brings the entire architecture demo together. It defines all four services (flight-status, gate-info, weather, aviation-mcp), their networking, health checks, and startup ordering. This is the "one command to run everything" deliverable.

##### Task Purpose
**As a** developer or demo operator
**I need** a docker-compose.yml that starts all services with proper ordering
**So that** the full architecture demo runs with `docker-compose up --build`

##### Dependencies
- **Prerequisite Tasks**: Phase 1 (C# services with Dockerfiles), Phase 2 (MCP server with Dockerfile)
- **Parallel Tasks**: T-302, T-303 (can be worked on simultaneously)
- **Integration Points**: All 4 Dockerfiles (3 C# + 1 Python), Docker networking
- **Blocked By**: None (Dockerfiles exist from Phase 1 and Phase 2)

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When `docker-compose up --build` is run, the system shall build and start all 4 services
- **REQ-2**: While C# services are starting, the MCP server shall wait until all C# health checks pass before starting
- **REQ-3**: Where services communicate across containers, the system shall use Docker service names as hostnames (e.g., `http://flight-status:5001`)

##### Non-Functional Requirements
- **Performance**: Health check interval 10s, timeout 5s, 5 retries (50s max startup wait per service)
- **Networking**: All services on a shared bridge network (`aviation-net`)

##### Technical Constraints
- **Technology Stack**: Docker Compose (modern format, no `version:` field)
- **Architecture Patterns**: Service-per-container, health check-based startup ordering
- **Code Standards**: YAML best practices, comments for each service section

#### Implementation Details

##### Files to Modify/Create
```
docker-compose.yml  -- NEW: Full stack orchestration file at project root
```

##### Key Implementation Steps
1. **Define C# services** (flight-status, gate-info, weather) with build contexts pointing to `./src/{service}/`, port mappings, health checks, and network attachment
2. **Define aviation-mcp service** with build context `./src/aviation-mcp/`, environment variables for C# service URLs using Docker hostnames, `depends_on` with `condition: service_healthy` for all 3 C# services
3. **Define aviation-net network** as bridge driver
4. **Validate** with `docker-compose config`

##### Code Patterns to Follow
```yaml
# Pattern: Health check for C# ASP.NET Core services
# Install curl in Dockerfile or use wget. Alternative: use dotnet-based health check.
# Simplest: curl against the API endpoint
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:{port}/api/{endpoint}"]
  interval: 10s
  timeout: 5s
  retries: 5

# Pattern: depends_on with health condition
depends_on:
  flight-status:
    condition: service_healthy
  gate-info:
    condition: service_healthy
  weather:
    condition: service_healthy

# Pattern: Environment variables for Docker service discovery
environment:
  - FLIGHT_STATUS_URL=http://flight-status:5001
  - GATE_INFO_URL=http://gate-info:5002
  - WEATHER_URL=http://weather:5003
  - MCP_DEBUG=true
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Full stack startup
  Given all Dockerfiles exist for the 4 services
  When docker-compose up --build is executed
  Then all 4 services start successfully
  And C# services pass health checks before MCP server starts

Scenario 2: Service networking
  Given all services are running via docker-compose
  When the MCP server calls http://flight-status:5001/api/flights
  Then the request resolves via Docker DNS and returns data

Scenario 3: Syntax validation
  Given the docker-compose.yml file exists
  When docker-compose config is executed
  Then no errors are reported and the resolved config is printed

Scenario 4: Clean shutdown
  Given all services are running
  When docker-compose down is executed
  Then all containers stop and are removed cleanly
```

##### Rule-Based Criteria (Checklist)
- [ ] docker-compose.yml exists at project root
- [ ] Four services defined: flight-status, gate-info, weather, aviation-mcp
- [ ] Port mappings: 5001:5001, 5002:5002, 5003:5003, 8000:8000
- [ ] Health checks on all 3 C# services
- [ ] aviation-mcp depends_on all 3 C# services with condition: service_healthy
- [ ] Environment variables pass service URLs to aviation-mcp
- [ ] MCP_DEBUG=true set for aviation-mcp
- [ ] aviation-net bridge network defined and attached to all services
- [ ] `docker-compose config` validates without errors
- [ ] No deprecated `version:` field (modern compose format)

#### Validation & Quality Gates

##### Code Quality Checks
```bash
# Validate compose file syntax
docker-compose config

# Verify all services defined
docker-compose config --services
# Expected output: flight-status, gate-info, weather, aviation-mcp
```

##### Definition of Done
- [ ] docker-compose.yml created at project root
- [ ] `docker-compose config` passes
- [ ] All 4 services listed in config output
- [ ] Health checks configured for C# services
- [ ] Startup ordering enforced via depends_on conditions

#### Resources & References

##### Documentation Links
- **Docker Compose Spec**: https://docs.docker.com/compose/compose-file/ -- Service definition, depends_on, healthcheck
- **Phase 1 PRP**: docs/prps/phase1-csharp-microservices.md -- C# service ports, Dockerfile patterns
- **Phase 2 PRP**: docs/prps/phase2-python-mcp-server.md -- MCP server Dockerfile, environment variables

#### Notes & Comments

##### Implementation Notes
- The C# service Dockerfiles may not include `curl` by default. If health checks fail because curl is not present, either install curl in the Dockerfile runtime stage or switch to a TCP-based health check (`test: ["CMD-SHELL", "dotnet --info || exit 1"]`). However, the preferred approach is HTTP health checks against the actual API endpoints to verify the application is truly ready, not just the container running.
- The CLI client is NOT included in docker-compose -- it runs on the host machine connecting to `localhost:8000`.

---

### T-302: Create aviation-mcp-client Project with pyproject.toml

**Task ID**: T-302
**Task Name**: Create aviation-mcp-client Project with pyproject.toml
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase3-cli-test-client.md](/Users/owenmccusker/Documents/dev/claude/py-cs-aviation-mcp-claude/docs/prps/phase3-cli-test-client.md) -- Task 2

##### Feature Overview
Scaffolds the Python project for the CLI test client with all required dependencies. This is the foundation for all subsequent client tasks.

##### Task Purpose
**As a** developer
**I need** a properly configured Python project with all dependencies installed
**So that** I can build the LangChain agent and test runner modules

##### Dependencies
- **Prerequisite Tasks**: None
- **Parallel Tasks**: T-301, T-303 (can be worked on simultaneously)
- **Integration Points**: uv package manager, PyPI packages
- **Blocked By**: None

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When `uv sync` is run in the project directory, all dependencies shall install successfully
- **REQ-2**: The project shall include both runtime and development dependencies

##### Technical Constraints
- **Technology Stack**: Python 3.13, uv package manager
- **Key Dependencies**:
  - `langchain>=0.3.0`
  - `langgraph>=0.2.0`
  - `langchain-mcp-adapters>=0.1.0`
  - `langchain-anthropic` (for Claude as default LLM)
  - `langchain-openai` (optional alternative)
  - `mcp>=1.25,<2`
  - Dev: `pytest`, `pytest-asyncio`, `ruff`

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp-client/
  pyproject.toml          -- NEW: uv project configuration with all dependencies
  src/
    __init__.py            -- NEW: Package init (empty)
  tests/
    __init__.py            -- NEW: Test package init (empty)
```

##### Key Implementation Steps
1. **Create directory structure**: `src/aviation-mcp-client/src/` and `src/aviation-mcp-client/tests/`
2. **Create pyproject.toml** with project metadata, runtime dependencies, and dev dependency group
3. **Create `__init__.py` files** for src and tests packages
4. **Run `uv sync`** to install all dependencies and verify resolution

##### Code Patterns to Follow
```toml
# Pattern: pyproject.toml for uv project (matching Phase 2 aviation-mcp style)
[project]
name = "aviation-mcp-client"
version = "0.1.0"
description = "LangChain CLI test client for Aviation MCP server"
requires-python = ">=3.13"
dependencies = [
    "langchain>=0.3.0",
    "langgraph>=0.2.0",
    "langchain-mcp-adapters>=0.1.0",
    "langchain-anthropic>=0.3.0",
    "mcp>=1.25,<2",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "ruff>=0.8",
]
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Dependency installation
  Given the pyproject.toml exists with all dependencies listed
  When uv sync is run in src/aviation-mcp-client/
  Then all dependencies install without errors
  And a uv.lock file is created

Scenario 2: Import verification
  Given dependencies are installed
  When python -c "import langchain; import langgraph; import mcp" is run
  Then no import errors occur
```

##### Rule-Based Criteria (Checklist)
- [ ] Directory structure created: src/aviation-mcp-client/src/ and tests/
- [ ] pyproject.toml contains all required runtime dependencies
- [ ] pyproject.toml contains dev dependency group with pytest and ruff
- [ ] `__init__.py` files created for src and tests packages
- [ ] `uv sync` completes successfully
- [ ] Python version requirement set to >=3.13

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp-client
uv sync
# Expected: All dependencies resolve and install

uv run python -c "import langchain; import langgraph; import mcp; print('OK')"
# Expected: OK
```

##### Definition of Done
- [ ] Project directory structure created
- [ ] pyproject.toml with all dependencies
- [ ] `uv sync` succeeds
- [ ] Core imports work

---

### T-303: Create Configuration Module

**Task ID**: T-303
**Task Name**: Create Configuration Module
**Priority**: High

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase3-cli-test-client.md](/Users/owenmccusker/Documents/dev/claude/py-cs-aviation-mcp-claude/docs/prps/phase3-cli-test-client.md) -- Task 3

##### Feature Overview
Centralized configuration for the CLI client: MCP server URL, LLM provider settings, and batch mode flag. All values configurable via environment variables with sensible defaults.

##### Task Purpose
**As a** developer running the CLI client
**I need** configurable MCP server URL and LLM settings
**So that** the client works both locally (`localhost:8000`) and against Docker-hosted services

##### Dependencies
- **Prerequisite Tasks**: T-302 (project must exist with dependencies)
- **Parallel Tasks**: T-301 (independent)
- **Integration Points**: Environment variables, LLM provider APIs
- **Blocked By**: None

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When MCP_SERVER_URL environment variable is set, the system shall use it as the MCP server endpoint
- **REQ-2**: When no environment variable is set, the system shall default to `http://localhost:8000/sse`
- **REQ-3**: When LLM_PROVIDER is "anthropic", the system shall use ChatAnthropic; when "openai", ChatOpenAI

##### Technical Constraints
- **Technology Stack**: Python dataclass or simple class, os.environ for env vars
- **Code Standards**: No external config library needed; keep it simple

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp-client/src/config.py  -- NEW: Configuration class with env var loading
```

##### Key Implementation Steps
1. **Create Config dataclass** with fields: `mcp_url`, `llm_provider`, `llm_model`, `llm_api_key`
2. **Load from environment variables** with defaults: MCP_SERVER_URL, LLM_PROVIDER, LLM_MODEL, LLM_API_KEY
3. **Implement `get_chat_model()` method** that returns the appropriate LangChain chat model instance
4. **Validate** that LLM API key is present when interactive mode is used (not needed for batch)

##### Code Patterns to Follow
```python
# Pattern: Config class with environment variable loading
import os
from dataclasses import dataclass, field

@dataclass
class Config:
    mcp_url: str = field(default_factory=lambda: os.getenv("MCP_SERVER_URL", "http://localhost:8000/sse"))
    llm_provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "anthropic"))
    llm_model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "claude-sonnet-4-5-20250929"))
    llm_api_key: str = field(default_factory=lambda: os.getenv("LLM_API_KEY", ""))

    def get_chat_model(self):
        if self.llm_provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model=self.llm_model, api_key=self.llm_api_key)
        elif self.llm_provider == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model=self.llm_model, api_key=self.llm_api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Default configuration
  Given no environment variables are set
  When Config() is instantiated
  Then mcp_url is "http://localhost:8000/sse"
  And llm_provider is "anthropic"

Scenario 2: Environment variable override
  Given MCP_SERVER_URL="http://aviation-mcp:8000/sse" is set
  When Config() is instantiated
  Then mcp_url is "http://aviation-mcp:8000/sse"

Scenario 3: Chat model creation
  Given Config with llm_provider="anthropic" and a valid API key
  When get_chat_model() is called
  Then a ChatAnthropic instance is returned

Scenario 4: Unsupported provider
  Given Config with llm_provider="unsupported"
  When get_chat_model() is called
  Then a ValueError is raised
```

##### Rule-Based Criteria (Checklist)
- [ ] Config class created with all required fields
- [ ] Environment variable loading with defaults
- [ ] `get_chat_model()` supports anthropic and openai providers
- [ ] Error raised for unsupported LLM provider
- [ ] mcp_url accepts CLI argument override (used by client.py)
- [ ] No hardcoded API keys

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp-client
uv run ruff check src/config.py
uv run python -c "from src.config import Config; c = Config(); print(c.mcp_url)"
# Expected: http://localhost:8000/sse
```

##### Definition of Done
- [ ] config.py created with Config dataclass
- [ ] All fields load from environment variables
- [ ] `get_chat_model()` works for anthropic provider
- [ ] Ruff passes with no errors

---

### T-304: Create LangChain Agent Setup Module

**Task ID**: T-304
**Task Name**: Create LangChain Agent Setup Module
**Priority**: High

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase3-cli-test-client.md](/Users/owenmccusker/Documents/dev/claude/py-cs-aviation-mcp-claude/docs/prps/phase3-cli-test-client.md) -- Task 4

##### Feature Overview
The agent module connects to the MCP server via SSE using `langchain-mcp-adapters`, loads available MCP tools, and creates a LangGraph ReAct agent. This agent is used by the interactive REPL mode to route natural language queries to the appropriate MCP tools.

##### Task Purpose
**As a** user in interactive REPL mode
**I need** a LangChain agent that understands available MCP tools
**So that** I can ask natural language questions and get aviation data back

##### Dependencies
- **Prerequisite Tasks**: T-302 (dependencies installed), T-303 (config module)
- **Parallel Tasks**: T-305 (batch test runner is independent of agent)
- **Integration Points**: MCP server SSE endpoint, LLM provider API, langchain-mcp-adapters
- **Blocked By**: None

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When the agent module is initialized, it shall connect to the MCP server via SSE and load all available tools
- **REQ-2**: When a user query is sent to the agent, it shall route to the appropriate MCP tool and return the result
- **REQ-3**: The agent shall use `create_react_agent` from LangGraph for tool-calling behavior

##### Technical Constraints
- **Technology Stack**: langchain-mcp-adapters (`MultiServerMCPClient`), LangGraph (`create_react_agent`)
- **Architecture Patterns**: Async context manager pattern for MCP client connection
- **Critical Gotcha**: `MultiServerMCPClient` is an async context manager -- the agent and tools are only valid within the `async with` block. The REPL loop must run inside this context.

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp-client/src/agent.py  -- NEW: LangChain agent setup with MCP tool loading
```

##### Key Implementation Steps
1. **Create `create_aviation_agent` async function** that accepts a Config object
2. **Initialize `MultiServerMCPClient`** with the MCP server URL and SSE transport
3. **Load tools** via `client.get_tools()` inside the async context
4. **Create ReAct agent** using `create_react_agent(model, tools)` from LangGraph
5. **Return the agent executor** for use by the REPL loop (IMPORTANT: must be used within the client context)

##### Code Patterns to Follow
```python
# Pattern: MCP client + agent creation
# CRITICAL: The agent must be used WITHIN the MultiServerMCPClient context
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

async def create_mcp_client_and_agent(config):
    """Create MCP client and agent. Returns (client, agent) tuple.
    Caller must use client as async context manager."""
    client = MultiServerMCPClient({
        "aviation-mcp": {
            "url": config.mcp_url,
            "transport": "sse",
        }
    })
    return client

async def run_agent_loop(config):
    """Run the agent within the MCP client context."""
    client = MultiServerMCPClient({
        "aviation-mcp": {
            "url": config.mcp_url,
            "transport": "sse",
        }
    })
    async with client as c:
        tools = c.get_tools()
        model = config.get_chat_model()
        agent = create_react_agent(model, tools)
        # Agent is valid here -- run the REPL loop inside this context
        yield agent  # or pass agent to callback
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Agent creation
  Given the MCP server is running on port 8000
  And a valid LLM API key is configured
  When the agent module creates an agent
  Then the agent has access to 3 MCP tools (get_flight_status, get_gate_info, get_weather)

Scenario 2: Tool invocation via agent
  Given a running agent connected to the MCP server
  When the agent receives query "What flights are at BDL?"
  Then the agent calls the get_flight_status tool with airport=BDL
  And returns flight data to the user

Scenario 3: MCP server unavailable
  Given the MCP server is not running
  When the agent module attempts to connect
  Then a connection error is raised with a descriptive message
```

##### Rule-Based Criteria (Checklist)
- [ ] agent.py created with async function for agent creation
- [ ] Uses `MultiServerMCPClient` with SSE transport configuration
- [ ] Uses `create_react_agent` from langgraph.prebuilt
- [ ] Agent is created within the async context manager scope
- [ ] Tools loaded via `client.get_tools()`
- [ ] Chat model obtained from Config.get_chat_model()
- [ ] Connection errors handled gracefully with descriptive messages
- [ ] Module is fully async (no blocking calls)

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp-client
uv run ruff check src/agent.py
# Expected: No errors

# Manual validation (requires MCP server running):
# uv run python -c "import asyncio; from src.agent import ...; asyncio.run(...)"
```

##### Definition of Done
- [ ] agent.py created with full agent setup logic
- [ ] Async context manager pattern correctly implemented
- [ ] Error handling for MCP server unavailability
- [ ] Ruff passes

#### Resources & References

##### Documentation Links
- **langchain-mcp-adapters**: https://github.com/langchain-ai/langchain-mcp-adapters -- MultiServerMCPClient API
- **LangGraph create_react_agent**: https://python.langchain.com/api_reference/langchain/agents/langchain.agents.react.agent.create_react_agent.html

##### Implementation Notes
- The `MultiServerMCPClient` context manager manages the SSE connection lifecycle. When the context exits, the connection closes. Therefore, the interactive REPL loop MUST run inside the `async with` block. Do not try to return the agent and use it outside the context.
- `create_react_agent` requires a **chat model** (ChatAnthropic, ChatOpenAI), not a base LLM. Ensure Config.get_chat_model() returns the correct type.

---

### T-305: Create Batch Test Runner

**Task ID**: T-305
**Task Name**: Create Batch Test Runner
**Priority**: High

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase3-cli-test-client.md](/Users/owenmccusker/Documents/dev/claude/py-cs-aviation-mcp-claude/docs/prps/phase3-cli-test-client.md) -- Task 5

##### Feature Overview
The batch test runner provides automated, CI-friendly integration validation. It connects directly to the MCP server via SSE (bypassing the LangChain agent/LLM), runs predefined test scenarios against all three tools, and reports pass/fail results. This is the key automated validation component.

##### Task Purpose
**As a** CI pipeline or developer running integration tests
**I need** automated test scenarios that exercise all MCP tools without an LLM
**So that** I can validate the full stack works end-to-end with a single command

##### Dependencies
- **Prerequisite Tasks**: T-302 (dependencies installed), T-303 (config module)
- **Parallel Tasks**: T-304 (agent setup is independent)
- **Integration Points**: MCP server SSE endpoint (direct connection, no LLM)
- **Blocked By**: None

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When `--test` flag is passed, the system shall run all predefined test scenarios
- **REQ-2**: When all scenarios pass, the system shall exit with code 0
- **REQ-3**: When any scenario fails, the system shall exit with code 1
- **REQ-4**: Each scenario shall print its name, tool invoked, and PASS/FAIL status

##### Non-Functional Requirements
- **Performance**: All scenarios should complete within 30 seconds against a running stack
- **No LLM required**: Batch mode connects directly to MCP server via `mcp.client.sse.sse_client`

##### Technical Constraints
- **Technology Stack**: MCP Python SDK client (`mcp.client.sse.sse_client`, `mcp.ClientSession`)
- **Critical Design Decision**: Batch mode does NOT use LangChain agent. It calls MCP tools directly via `session.call_tool()`. This eliminates the LLM API key requirement for automated testing.

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp-client/src/test_runner.py  -- NEW: Batch test runner with predefined scenarios
```

##### Key Implementation Steps
1. **Define `TestScenario` dataclass** with fields: name, tool_name, params, expected_check, expected_value
2. **Define `TEST_SCENARIOS` list** covering all 3 tools with positive and negative cases (8 scenarios per PRP)
3. **Implement `run_batch_tests(config)` async function** that connects to MCP server via SSE, iterates scenarios, calls tools, and validates results
4. **Implement `check_result()` validation function** supporting checks: "non_empty", "empty", "contains_field"
5. **Print formatted results** with [PASS]/[FAIL] prefixes and summary at end

##### Code Patterns to Follow
```python
# Pattern: Direct MCP client connection (no LLM)
from mcp.client.sse import sse_client
from mcp import ClientSession
from dataclasses import dataclass

@dataclass
class TestScenario:
    name: str
    tool_name: str
    params: dict
    expected_check: str  # "non_empty", "empty", "contains_field"
    expected_value: str | None = None

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

async def run_batch_tests(config) -> bool:
    async with sse_client(config.mcp_url) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            all_passed = True
            for scenario in TEST_SCENARIOS:
                result = await session.call_tool(scenario.tool_name, scenario.params)
                passed = check_result(result, scenario)
                status = "PASS" if passed else "FAIL"
                print(f"  [{status}] {scenario.name}")
                if not passed:
                    all_passed = False
            return all_passed
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: All tests pass
  Given the MCP server and all C# services are running
  When run_batch_tests() is called
  Then all 8 test scenarios report PASS
  And the function returns True

Scenario 2: Non-empty result validation
  Given the MCP server is running
  When get_flight_status is called with airport=BDL
  Then the result contains flight data (non-empty)

Scenario 3: Empty result validation
  Given the MCP server is running
  When get_flight_status is called with airport=XXX
  Then the result is empty (no flights for unknown airport)

Scenario 4: Failure reporting
  Given the MCP server returns unexpected results for a scenario
  When the check fails
  Then [FAIL] is printed for that scenario
  And the function returns False

Scenario 5: MCP server unavailable
  Given the MCP server is not running
  When run_batch_tests() is called
  Then a connection error is reported gracefully
```

##### Rule-Based Criteria (Checklist)
- [ ] TestScenario dataclass defined with all fields
- [ ] 8 test scenarios defined covering all 3 tools (flights, gates, weather)
- [ ] Positive tests (known airports) and negative tests (unknown airports/gates)
- [ ] Direct MCP client connection (no LLM dependency)
- [ ] check_result() supports "non_empty" and "empty" validation modes
- [ ] Formatted output with [PASS]/[FAIL] per scenario
- [ ] Summary printed at end (X/Y passed)
- [ ] Returns bool (True=all pass, False=any fail)
- [ ] Connection error handling

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp-client
uv run ruff check src/test_runner.py
# Expected: No errors
```

##### Definition of Done
- [ ] test_runner.py created with TestScenario, TEST_SCENARIOS, and run_batch_tests
- [ ] All 8 scenarios from PRP implemented
- [ ] Ruff passes
- [ ] Manual test against running stack passes all scenarios

#### Notes & Comments

##### Implementation Notes
- The `session.call_tool()` return type from the MCP SDK is a `CallToolResult` object. Check its `.content` attribute for the tool's response data. The content is typically a list of `TextContent` objects with `.text` containing JSON strings.
- The test scenarios reference specific airports (BDL, JFK, LAX) and flight numbers that must match the stub data in Phase 1 C# services. Verify the JSON stub files have matching records.

---

### T-306: Create CLI Entry Point with REPL and Batch Modes

**Task ID**: T-306
**Task Name**: Create CLI Entry Point with REPL and Batch Modes
**Priority**: High

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase3-cli-test-client.md](/Users/owenmccusker/Documents/dev/claude/py-cs-aviation-mcp-claude/docs/prps/phase3-cli-test-client.md) -- Task 6

##### Feature Overview
The main entry point for the CLI client. Handles argument parsing, dispatches to either interactive REPL mode (default) or batch test mode (--test). The REPL provides a prompt-based interface where users type natural language queries and get aviation data back via the LangChain agent.

##### Task Purpose
**As a** user or developer
**I need** a single CLI entry point with both interactive and batch modes
**So that** I can demo the system interactively or validate it automatically

##### Dependencies
- **Prerequisite Tasks**: T-303 (config), T-304 (agent), T-305 (test runner)
- **Parallel Tasks**: None (depends on all core modules)
- **Integration Points**: agent.py (REPL mode), test_runner.py (batch mode), config.py
- **Blocked By**: T-304 and T-305 must be complete

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When invoked with no arguments, the system shall start interactive REPL mode
- **REQ-2**: When invoked with `--test`, the system shall run batch tests and exit with appropriate code
- **REQ-3**: When `--mcp-url` is provided, the system shall use the specified MCP server URL
- **REQ-4**: When user types "quit" or "exit" in REPL, the system shall exit cleanly
- **REQ-5**: When Ctrl+C is pressed, the system shall exit gracefully without traceback

##### Technical Constraints
- **Technology Stack**: argparse for CLI, asyncio.run for async entry
- **Critical Gotcha**: `input()` is blocking. In the async REPL loop, either use `asyncio.get_event_loop().run_in_executor(None, input, prompt)` or accept that `input()` blocks the event loop (acceptable for a demo CLI).

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp-client/src/client.py  -- NEW: Main CLI entry point with argument parsing and REPL loop
```

##### Key Implementation Steps
1. **Set up argparse** with `--test` (batch mode flag), `--mcp-url` (server URL override)
2. **Create Config** from CLI args, merging with environment variables
3. **Dispatch to batch or interactive mode** based on `--test` flag
4. **Implement interactive REPL loop** inside the MCP client async context:
   - Print welcome message
   - Loop: read input, send to agent, print response
   - Handle quit/exit commands
   - Handle Ctrl+C (KeyboardInterrupt)
5. **Implement batch mode dispatch** calling `run_batch_tests(config)` and exiting with appropriate code

##### Code Patterns to Follow
```python
# Pattern: CLI entry point with dual modes
import argparse
import asyncio
from src.config import Config
from src.test_runner import run_batch_tests

async def interactive_mode(config: Config):
    """Run interactive REPL with LangChain agent."""
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langgraph.prebuilt import create_react_agent

    client = MultiServerMCPClient({
        "aviation-mcp": {
            "url": config.mcp_url,
            "transport": "sse",
        }
    })
    async with client as c:
        tools = c.get_tools()
        model = config.get_chat_model()
        agent = create_react_agent(model, tools)

        print("Aviation MCP Client (type 'quit' to exit)")
        print(f"Connected to MCP server at {config.mcp_url}")
        print(f"Tools available: {[t.name for t in tools]}")
        print()

        while True:
            try:
                query = input("> ")
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            if query.strip().lower() in ("quit", "exit"):
                print("Goodbye!")
                break
            if not query.strip():
                continue

            result = await agent.ainvoke({"messages": [("user", query)]})
            print(result["messages"][-1].content)
            print()

async def main():
    parser = argparse.ArgumentParser(description="Aviation MCP Test Client")
    parser.add_argument("--test", action="store_true", help="Run batch tests")
    parser.add_argument("--mcp-url", default=None, help="MCP server SSE URL")
    args = parser.parse_args()

    config = Config()
    if args.mcp_url:
        config.mcp_url = args.mcp_url

    if args.test:
        success = await run_batch_tests(config)
        raise SystemExit(0 if success else 1)
    else:
        await interactive_mode(config)

if __name__ == "__main__":
    asyncio.run(main())
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Interactive mode startup
  Given the MCP server is running and LLM API key is configured
  When client.py is run with no arguments
  Then a welcome message is printed with available tools
  And the REPL prompt ">" appears

Scenario 2: Interactive query
  Given the REPL is running
  When user types "What flights are at BDL?"
  Then the agent calls get_flight_status and displays flight data

Scenario 3: REPL exit
  Given the REPL is running
  When user types "quit"
  Then the program exits cleanly with code 0

Scenario 4: Ctrl+C handling
  Given the REPL is running
  When Ctrl+C is pressed
  Then the program prints "Goodbye!" and exits without traceback

Scenario 5: Batch mode
  Given the MCP server and C# services are running
  When client.py --test is run
  Then all batch test scenarios execute
  And exit code is 0 if all pass, 1 if any fail

Scenario 6: Custom MCP URL
  Given the MCP server is running on a non-default URL
  When client.py --mcp-url http://custom:9000/sse is run
  Then the client connects to the specified URL
```

##### Rule-Based Criteria (Checklist)
- [ ] client.py created as main entry point
- [ ] argparse with --test and --mcp-url arguments
- [ ] Interactive mode: REPL loop with prompt, agent query, result display
- [ ] Batch mode: dispatches to run_batch_tests, exits with correct code
- [ ] Welcome message shows connected URL and available tools
- [ ] "quit" and "exit" commands work
- [ ] Ctrl+C and EOF handled gracefully
- [ ] Empty input lines are ignored (no agent call)
- [ ] REPL loop runs inside MCP client async context
- [ ] `asyncio.run(main())` as entry point

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp-client
uv run ruff check src/client.py
# Expected: No errors

# Batch mode validation (requires running stack):
uv run python -m src.client --test --mcp-url http://localhost:8000/sse
# Expected: All scenarios PASS, exit code 0
```

##### Definition of Done
- [ ] client.py created with both modes
- [ ] argparse configured correctly
- [ ] REPL loop functional with graceful exit
- [ ] Batch mode dispatches correctly
- [ ] Ruff passes

---

### T-307: Create pytest Unit Tests

**Task ID**: T-307
**Task Name**: Create pytest Unit Tests for Client Module
**Priority**: Medium

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase3-cli-test-client.md](/Users/owenmccusker/Documents/dev/claude/py-cs-aviation-mcp-claude/docs/prps/phase3-cli-test-client.md) -- Task 7

##### Feature Overview
Unit tests for the CLI client module, covering the batch test runner logic and config module. Tests use mocked MCP responses to avoid requiring a running MCP server.

##### Task Purpose
**As a** developer maintaining the CLI client
**I need** automated unit tests that run without external services
**So that** I can verify client logic works correctly in isolation

##### Dependencies
- **Prerequisite Tasks**: T-302 (project setup), T-303 (config), T-305 (test runner)
- **Parallel Tasks**: None
- **Integration Points**: pytest, pytest-asyncio, unittest.mock
- **Blocked By**: T-305 (test_runner must be implemented to test it)

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When `uv run pytest` is run, all unit tests shall pass
- **REQ-2**: Tests shall not require a running MCP server or LLM API key
- **REQ-3**: Tests shall cover config loading, test scenario validation logic, and result checking

##### Technical Constraints
- **Technology Stack**: pytest, pytest-asyncio, unittest.mock (for mocking MCP client)
- **Code Standards**: Follow Phase 2 test patterns from `src/aviation-mcp/tests/`

#### Implementation Details

##### Files to Modify/Create
```
src/aviation-mcp-client/tests/test_client.py  -- NEW: Unit tests for client modules
```

##### Key Implementation Steps
1. **Test Config class**: Default values, environment variable overrides, get_chat_model validation
2. **Test TestScenario and check_result**: Verify result validation logic for "non_empty" and "empty" checks
3. **Test run_batch_tests with mocked MCP session**: Mock `sse_client` and `ClientSession` to simulate tool responses
4. **Test argument parsing** (optional): Verify CLI args are parsed correctly

##### Code Patterns to Follow
```python
# Pattern: pytest-asyncio for async tests
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.fixture
def config():
    from src.config import Config
    return Config(mcp_url="http://test:8000/sse")

def test_config_defaults():
    from src.config import Config
    config = Config()
    assert config.mcp_url == "http://localhost:8000/sse"
    assert config.llm_provider == "anthropic"

def test_check_result_non_empty():
    from src.test_runner import check_result, TestScenario
    scenario = TestScenario("test", "tool", {}, "non_empty")
    # Mock a non-empty result
    result = MagicMock()
    result.content = [MagicMock(text='[{"airport": "BDL"}]')]
    assert check_result(result, scenario) is True

def test_check_result_empty():
    from src.test_runner import check_result, TestScenario
    scenario = TestScenario("test", "tool", {}, "empty")
    result = MagicMock()
    result.content = [MagicMock(text='[]')]
    assert check_result(result, scenario) is True

@pytest.mark.asyncio
async def test_batch_tests_all_pass():
    # Mock the MCP client session
    with patch("src.test_runner.sse_client") as mock_sse:
        mock_session = AsyncMock()
        mock_session.initialize = AsyncMock()
        mock_session.call_tool = AsyncMock(return_value=mock_non_empty_result())
        # ... setup context managers ...
        result = await run_batch_tests(config)
        assert result is True
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: All tests pass
  Given test_client.py exists with unit tests
  When uv run pytest tests/ -v is executed
  Then all tests pass

Scenario 2: Config default values
  Given no environment variables are set
  When Config() is tested
  Then default MCP URL and LLM provider are correct

Scenario 3: Result validation logic
  Given a mock MCP tool result with flight data
  When check_result is called with expected_check="non_empty"
  Then it returns True

Scenario 4: Empty result validation
  Given a mock MCP tool result with empty data
  When check_result is called with expected_check="empty"
  Then it returns True
```

##### Rule-Based Criteria (Checklist)
- [ ] test_client.py created in tests/ directory
- [ ] Tests for Config class (defaults, env vars, get_chat_model)
- [ ] Tests for check_result() validation logic
- [ ] Tests for TestScenario dataclass
- [ ] Async tests use @pytest.mark.asyncio decorator
- [ ] All external dependencies mocked (no real MCP or LLM connections)
- [ ] `uv run pytest tests/ -v` passes all tests

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/aviation-mcp-client
uv run ruff check tests/
uv run pytest tests/ -v
# Expected: All tests pass, no lint errors
```

##### Definition of Done
- [ ] test_client.py created with comprehensive unit tests
- [ ] `uv run pytest` passes all tests
- [ ] No external service dependencies in tests
- [ ] Ruff passes on test files

---

### T-308: Full Stack Integration Test

**Task ID**: T-308
**Task Name**: Full Stack Integration Test via Docker Compose
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase3-cli-test-client.md](/Users/owenmccusker/Documents/dev/claude/py-cs-aviation-mcp-claude/docs/prps/phase3-cli-test-client.md) -- Task 8

##### Feature Overview
The final integration test that validates the entire architecture works end-to-end: docker-compose brings up all services, the CLI client connects and exercises all tools, debug logs confirm protocol traces. This is the "capstone" validation that proves the full stack.

##### Task Purpose
**As a** project stakeholder
**I need** proof that the full architecture works end-to-end
**So that** the architectural demonstration is complete and validated

##### Dependencies
- **Prerequisite Tasks**: ALL previous tasks (T-301 through T-307)
- **Parallel Tasks**: None (final integration step)
- **Integration Points**: Docker Compose, all 4 services, CLI client, MCP protocol
- **Blocked By**: All code must be complete and unit tests passing

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When `docker-compose up --build` is run, all 4 services shall start and become healthy
- **REQ-2**: When the batch test client runs against the Docker stack, all scenarios shall pass
- **REQ-3**: When debug mode is enabled, MCP server logs shall show protocol traces
- **REQ-4**: When `docker-compose down` is run, all containers shall stop and be removed

##### Non-Functional Requirements
- **Performance**: Full stack should be ready within 2 minutes of `docker-compose up --build`
- **Reliability**: Health checks ensure no premature connections

#### Implementation Details

##### Files to Modify/Create
```
No new files -- this is a validation/testing task against the existing codebase.
```

##### Key Implementation Steps
1. **Start full stack**: `docker-compose up --build -d`
2. **Wait for health checks**: `docker-compose ps` -- all services show "healthy"
3. **Run batch tests**: `cd src/aviation-mcp-client && uv run python -m src.client --test --mcp-url http://localhost:8000/sse`
4. **Verify all scenarios pass** with exit code 0
5. **Check debug logs**: `docker-compose logs aviation-mcp` -- verify JSON-RPC messages, tool registration, capability negotiation
6. **Manual interactive test** (optional): Run interactive mode, type a query, verify response
7. **Clean up**: `docker-compose down`
8. **Document any issues** and fix before marking complete

##### Validation Commands
```bash
# Step 1: Start stack
docker-compose up --build -d

# Step 2: Wait for healthy status (may need to poll)
docker-compose ps
# Expected: All services show "healthy" or "running"

# Step 3: Run batch tests from host
cd src/aviation-mcp-client
uv run python -m src.client --test --mcp-url http://localhost:8000/sse
# Expected: All 8 scenarios PASS, exit code 0
echo $?
# Expected: 0

# Step 4: Check protocol debug logs
docker-compose logs aviation-mcp | head -100
# Expected: JSON-RPC messages, tool registration, capability negotiation visible

# Step 5: Interactive mode test (manual)
uv run python -m src.client --mcp-url http://localhost:8000/sse
# Type: "What flights are at BDL?"
# Expected: Flight data displayed
# Type: "quit"

# Step 6: Clean up
docker-compose down
# Expected: All containers stopped and removed
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Full stack startup
  Given all Dockerfiles and docker-compose.yml are configured
  When docker-compose up --build is executed
  Then all 4 services start
  And C# services pass health checks
  And MCP server starts after C# services are healthy

Scenario 2: Batch test pass
  Given all services are running and healthy
  When the batch test client runs against localhost:8000
  Then all 8 test scenarios report PASS
  And exit code is 0

Scenario 3: Debug protocol trace
  Given services are running with MCP_DEBUG=true
  When batch tests are run (triggering tool calls)
  Then docker-compose logs aviation-mcp shows JSON-RPC messages
  And tool registration events are visible
  And capability negotiation is logged

Scenario 4: Interactive mode works
  Given all services are running
  And a valid LLM API key is configured
  When the interactive client sends "What flights are at BDL?"
  Then flight data for BDL is displayed

Scenario 5: Clean shutdown
  Given all services are running
  When docker-compose down is executed
  Then all containers stop cleanly
  And no orphan containers remain
```

##### Rule-Based Criteria (Checklist)
- [ ] `docker-compose up --build` starts all 4 services
- [ ] All C# services pass health checks
- [ ] MCP server starts after C# services are healthy
- [ ] CLI client connects to MCP server via SSE
- [ ] Batch mode: all 8 test scenarios pass with exit code 0
- [ ] Interactive mode: natural language queries return aviation data (manual test)
- [ ] Debug logs show full protocol trace (JSON-RPC, tool registration)
- [ ] `docker-compose down` cleans up cleanly
- [ ] pytest tests pass for client module (`uv run pytest`)
- [ ] Client handles MCP server unavailable gracefully (tested by stopping MCP container)

#### Validation & Quality Gates

##### Full Validation Sequence
```bash
# 1. Unit tests first
cd src/aviation-mcp-client
uv run pytest tests/ -v
# Expected: All pass

# 2. Lint check
uv run ruff check src/ tests/
# Expected: No errors

# 3. Docker compose validation
cd /path/to/project/root
docker-compose config
# Expected: Valid config output

# 4. Full stack integration
docker-compose up --build -d
sleep 60  # Wait for health checks
docker-compose ps  # Verify healthy
cd src/aviation-mcp-client
uv run python -m src.client --test --mcp-url http://localhost:8000/sse
# Expected: All PASS, exit 0

# 5. Debug log verification
docker-compose logs aviation-mcp | grep -i "json-rpc\|tool\|capability"
# Expected: Protocol trace entries found

# 6. Cleanup
docker-compose down
```

##### Definition of Done
- [ ] Full stack starts and all services are healthy
- [ ] Batch tests pass with exit code 0
- [ ] Debug logs contain protocol traces
- [ ] docker-compose down cleans up
- [ ] All PRP success criteria met

#### Resources & References

##### Documentation Links
- **Phase 1 PRP**: docs/prps/phase1-csharp-microservices.md -- C# service contracts and stub data
- **Phase 2 PRP**: docs/prps/phase2-python-mcp-server.md -- MCP server configuration, debug mode
- **Phase 3 PRP**: docs/prps/phase3-cli-test-client.md -- Full validation checklist

##### Implementation Notes
- If health checks fail due to missing `curl` in C# containers, the fix belongs in Phase 1 Dockerfiles (install curl in runtime stage: `RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*`).
- The test scenario airports (BDL, JFK, LAX) and flight numbers must match the JSON stub data created in Phase 1. If there is a mismatch, update either the test scenarios (T-305) or the stub data.
- Interactive mode testing requires a valid LLM API key set as LLM_API_KEY environment variable (or ANTHROPIC_API_KEY for the default Anthropic provider).

---

## Implementation Recommendations

### Suggested Team Structure
- **1 developer** can handle this entire phase sequentially (moderate complexity, 8 tasks)
- If splitting across 2 developers:
  - **Developer A**: T-301 (docker-compose), T-308 (integration test)
  - **Developer B**: T-302 through T-307 (all client code and unit tests)

### Optimal Task Sequencing

```
T-301 (docker-compose)  ----\
T-302 (project setup)  -----> T-303 (config) ----> T-304 (agent) --------\
                                    \----> T-305 (test runner) -----> T-306 (client.py) -> T-307 (tests) -> T-308 (integration)
```

**Recommended execution order**:
1. **T-301** + **T-302** (parallel -- no dependencies between them)
2. **T-303** (depends on T-302)
3. **T-304** + **T-305** (parallel -- both depend on T-303 only)
4. **T-306** (depends on T-304 + T-305)
5. **T-307** (depends on T-305 + T-306)
6. **T-308** (depends on everything)

### Parallelization Opportunities
- **T-301 and T-302** are fully independent -- can be done simultaneously
- **T-304 and T-305** are independent of each other (agent vs. batch runner) -- can be done simultaneously
- All other tasks have sequential dependencies

### Resource Allocation Suggestions
- **Estimated total effort**: 2-3 days for one experienced developer
- **Highest risk tasks**: T-304 (agent setup -- langchain-mcp-adapters version compatibility) and T-308 (integration -- multi-service Docker orchestration)
- **Quickest wins**: T-301 (docker-compose is well-documented pattern), T-302 (scaffolding), T-303 (simple config)

## Critical Path Analysis

### Tasks on Critical Path
```
T-302 -> T-303 -> T-305 -> T-306 -> T-307 -> T-308
```
(T-305 is on critical path because T-306 depends on both T-304 and T-305, and T-305 is more complex)

### Potential Bottlenecks
1. **T-304 (Agent Setup)**: `langchain-mcp-adapters` version compatibility with `mcp` SDK v1.x. If the adapter package has breaking changes or does not support the SSE transport correctly, this task could require significant debugging.
2. **T-308 (Integration)**: Docker health check timing. If C# services take too long to start, the MCP server may timeout waiting. Tune health check intervals if needed.
3. **Stub data mismatch**: If Phase 1 JSON stub data does not include the exact airports/flights referenced in T-305 test scenarios, batch tests will fail. Verify data alignment early.

### Schedule Optimization Suggestions
- Start T-301 and T-302 immediately in parallel to front-load infrastructure work
- Prototype T-304 (agent setup) early to identify any `langchain-mcp-adapters` compatibility issues before investing in the full implementation
- Run `docker-compose up --build` as soon as T-301 is done (even before client code) to validate the Docker infrastructure independently
- Use T-305 (batch test runner) as the primary validation tool throughout development -- it does not require an LLM API key and provides fast feedback

---

## Anti-Patterns to Avoid (from PRP)

- Do **not** require an LLM API key for batch testing -- batch mode calls tools directly via MCP client
- Do **not** hardcode the MCP server URL -- accept as CLI argument and env var
- Do **not** use synchronous HTTP clients -- everything is async
- Do **not** skip health checks in docker-compose -- services must be ready before dependent services start
- Do **not** run the CLI client inside Docker -- it is a local development/testing tool
