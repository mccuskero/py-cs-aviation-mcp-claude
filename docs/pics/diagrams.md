# Aviation MCP Diagrams

Mermaid source files (`.mmd`) and rendered PNGs for project documentation.

## Rendering

To regenerate PNGs from the Mermaid source files:

```bash
mmdc -i docs/pics/architecture.mmd -o docs/pics/architecture.png -b white -s 2
mmdc -i docs/pics/flow.mmd -o docs/pics/flow.png -b white -s 2
mmdc -i docs/pics/sequence.mmd -o docs/pics/sequence.png -b white -s 2
```

Requires [mermaid-cli](https://github.com/mermaid-js/mermaid-cli): `npm install -g @mermaid-js/mermaid-cli`

## Architecture Diagram

Shows the full system layout: CLI client, LLM providers, MCP server, C# microservices, and JSON stub data stores.

```mermaid
graph TB
    subgraph Client ["CLI Client (Host Machine)"]
        REPL["Interactive REPL<br/><i>LangChain ReAct Agent</i>"]
        BATCH["Batch Test Runner<br/><i>Direct MCP Calls</i>"]
    end

    subgraph LLM ["LLM Provider"]
        ANTHROPIC["Anthropic Claude"]
        OPENAI["OpenAI GPT-4o"]
        OLLAMA["Ollama Local Models"]
    end

    subgraph Docker ["Docker Compose (aviation-net)"]
        MCP["Aviation MCP Server<br/>Python 3.13 / FastMCP<br/>Port 8000 / SSE"]

        subgraph Services ["C# Microservices (.NET 9)"]
            FS["Flight Status :5001"]
            GI["Gate Info :5002"]
            WX["Weather :5003"]
        end
    end

    REPL -->|SSE| MCP
    BATCH -->|SSE| MCP
    REPL -.->|Tool Selection| LLM
    MCP -->|HTTP GET| FS
    MCP -->|HTTP GET| GI
    MCP -->|HTTP GET| WX
```

## Flow Diagram

Shows the request processing pipeline from user input through all layers to response output.

```mermaid
flowchart LR
    USER["User Query"] --> PARSE["client.py"]
    TEST["--test flag"] --> PARSE
    PARSE -->|Interactive| AGENT["LangChain Agent"]
    PARSE -->|Batch| RUNNER["Test Runner"]
    AGENT -->|MCP SSE| SSE["SSE :8000"]
    RUNNER -->|MCP SSE| SSE
    SSE --> TOOL["Tool Router"]
    TOOL --> HANDLER["Tool Handlers"]
    HANDLER --> HTTP["HTTP Clients"]
    HTTP -->|HTTP GET| CTRL["Controllers"]
    CTRL --> SVC["Service Layer"]
    SVC --> JSON["JSON Data"]
```

## Sequence Diagram

Shows the startup, batch test, and interactive mode request lifecycles with exact API calls.

```mermaid
sequenceDiagram
    actor User
    participant Client as CLI Client
    participant MCP as MCP Server (:8000)
    participant FS as Flight Status (:5001)

    User->>Client: python -m src.client --test
    Client->>MCP: SSE connect
    MCP-->>Client: Session initialized (3 tools)
    Client->>MCP: call_tool("get_flight_status", {airport: "BDL"})
    MCP->>FS: GET /api/flights?airport=BDL
    FS-->>MCP: 200 OK [{flight: "DL1234"}, ...]
    MCP-->>Client: [PASS] Non-empty result
    Client-->>User: Results: 8/8 passed
```
