# PRP: Phase 1 — Stubbed C# Microservices

## Discovery Summary

### Initial Task Analysis

Build three C# microservices (flight-status, gate-info, weather) as the backend layer of the Aviation MCP architectural demonstration. These services provide parameterized stubbed data from JSON files via REST APIs with Swagger documentation.

### User Clarifications Received

- **Question**: Minimal APIs or Controllers?
- **Answer**: Traditional Controller pattern with `[ApiController]` attribute
- **Impact**: Full layered structure (Controller → Service → Core) per microservice

- **Question**: How deep should stubbed data go?
- **Answer**: Parameterized stubs — load JSON, filter by input parameters, return matches or "not found"
- **Impact**: Services need actual filtering logic, not just hardcoded responses

- **Question**: Empty result HTTP response pattern?
- **Answer**: HTTP 200 with empty array for collection endpoints
- **Impact**: Controllers return `Ok(results)` always; empty `[]` when no matches

### Missing Requirements Identified

- Data model field definitions (proposed aviation-domain defaults)
- Port assignments per service (assigned: 5001, 5002, 5003)
- .gitignore needs C#/.NET entries added

## Goal

Create three independently deployable C# .NET 8 microservices — flight-status, gate-info, and weather — each following an identical Controller → Service → Core layered pattern. Each service loads parameterized stub data from JSON files, exposes a Swagger-documented REST API, includes xUnit tests, and runs in a Docker container.

The flight-status service is the pattern-setter; gate-info and weather replicate its structure.

## Why

- Provides the backend REST layer that the Python MCP server (Phase 2) will call
- Demonstrates enterprise C# microservice structure with clean layering
- Establishes the cross-language boundary (C# REST ↔ Python HTTP client) central to the architecture demo
- Parameterized stubs prove the contract works with real filtering, not just hardcoded responses

## What

### User-visible Behavior

Each microservice:
- Starts independently, listens on its assigned port
- Serves a Swagger UI at `/swagger`
- Responds to REST queries with filtered JSON data or empty arrays
- Returns proper HTTP status codes (200 for results/empty, 400 for bad requests)

### Success Criteria

- [ ] Three C# microservices build and run independently
- [ ] Each has Swagger UI accessible at `/swagger`
- [ ] Parameterized queries return correct filtered results
- [ ] Empty results return HTTP 200 with `[]`
- [ ] xUnit tests pass for service layer and controller layer
- [ ] Each service builds into a Docker image and runs in a container
- [ ] .gitignore updated with C#/.NET entries

## All Needed Context

### Research Phase Summary

- **Codebase patterns found**: None (greenfield project)
- **External research needed**: Yes — .NET 8 Controller scaffolding, Swashbuckle setup, Docker multi-stage builds
- **Knowledge gaps identified**: NuGet package versions, .NET 8 port defaults, solution structure

### Documentation & References

```yaml
- url: https://learn.microsoft.com/en-us/aspnet/core/web-api/?view=aspnetcore-8.0
  why: ASP.NET Core Controller pattern reference

- url: https://learn.microsoft.com/en-us/aspnet/core/tutorials/getting-started-with-swashbuckle?view=aspnetcore-8.0
  why: Swagger/Swashbuckle setup for .NET 8

- url: https://learn.microsoft.com/en-us/dotnet/core/docker/build-container
  why: .NET 8 Docker multi-stage build pattern

- url: https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/overview
  why: System.Text.Json deserialization for loading JSON stub data

- url: https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-sln
  why: Solution and project management CLI commands

- file: docs/brainstorm/brainstorm-initialize-20260209.md
  why: Architecture decisions, acceptance criteria, risk register

- file: CLAUDE.md
  why: Project conventions, directory structure, API endpoints
```

### Current Codebase Tree

```
py-cs-aviation-mcp-claude/
├── CLAUDE.md
├── README.md
├── LICENSE
├── .gitignore                    # Python-only, needs C# entries
├── .claude/settings.local.json
└── docs/
    ├── brainstorm/
    │   ├── project-start.md
    │   └── brainstorm-initialize-20260209.md
    └── templates/
        ├── prp_document_template.md
        ├── technical-task-template.md
        └── brainstorming_session_template.md
```

### Desired Codebase Tree (Phase 1 additions)

```
py-cs-aviation-mcp-claude/
├── .gitignore                           # UPDATED: add C#/.NET entries
├── src/
│   ├── flight-status/
│   │   ├── Dockerfile
│   │   └── src/
│   │       ├── FlightStatus.sln
│   │       ├── FLIGHTSTATUS.CLI/
│   │       │   ├── FLIGHTSTATUS.CLI.csproj
│   │       │   ├── Program.cs               # ASP.NET Core entry, Swagger config, DI
│   │       │   ├── Controllers/
│   │       │   │   └── FlightsController.cs  # [ApiController] with GET /api/flights
│   │       │   └── appsettings.json
│   │       ├── FLIGHTSTATUS.Core/
│   │       │   ├── FLIGHTSTATUS.Core.csproj
│   │       │   ├── Models/
│   │       │   │   └── Flight.cs             # Flight data model
│   │       │   └── Interfaces/
│   │       │       └── IFlightStatusService.cs
│   │       ├── FLIGHTSTATUS.Services/
│   │       │   ├── FLIGHTSTATUS.Services.csproj
│   │       │   ├── FlightStatusService.cs    # JSON loading + filtering logic
│   │       │   └── Data/
│   │       │       └── flights.json          # Stub data (3-5 airports)
│   │       └── FLIGHTSTATUS.Tests/
│   │           ├── FLIGHTSTATUS.Tests.csproj
│   │           ├── Services/
│   │           │   └── FlightStatusServiceTests.cs
│   │           └── Controllers/
│   │               └── FlightsControllerTests.cs
│   ├── gate-info/                           # Same layering as flight-status
│   │   ├── Dockerfile
│   │   └── src/
│   │       ├── GateInfo.sln
│   │       ├── GATEINFO.CLI/
│   │       ├── GATEINFO.Core/
│   │       ├── GATEINFO.Services/
│   │       └── GATEINFO.Tests/
│   └── weather/                             # Same layering as flight-status
│       ├── Dockerfile
│       └── src/
│           ├── Weather.sln
│           ├── WEATHER.CLI/
│           ├── WEATHER.Core/
│           ├── WEATHER.Services/
│           └── WEATHER.Tests/
```

### Known Gotchas & Library Quirks

```csharp
// CRITICAL: .NET 8 changed default port from 80 to 8080 in containers
// Must explicitly set port via ASPNETCORE_HTTP_PORTS env var in Dockerfile
// or via builder.WebHost.UseUrls() in Program.cs

// CRITICAL: Swashbuckle is no longer included by default in .NET 8 templates
// Must manually add NuGet package: Swashbuckle.AspNetCore v6.6.1+

// GOTCHA: System.Text.Json property naming defaults to camelCase in ASP.NET Core
// JSON stub files should use camelCase to match, or configure JsonSerializerOptions

// GOTCHA: For Docker, JSON data files must be copied into the container image
// Use COPY in Dockerfile and set CopyToOutputDirectory in .csproj
```

## Implementation Blueprint

### Data Models and Structure

```csharp
// === Flight Model (FLIGHTSTATUS.Core/Models/Flight.cs) ===
public class Flight
{
    public string Airport { get; set; }        // IATA code: "BDL", "JFK", etc.
    public string FlightNumber { get; set; }   // e.g., "1234"
    public string Airline { get; set; }        // e.g., "Delta"
    public string Origin { get; set; }         // IATA code
    public string Destination { get; set; }    // IATA code
    public string DepartureTime { get; set; }  // ISO 8601: "2026-02-09T14:30:00Z"
    public string ArrivalTime { get; set; }    // ISO 8601
    public string Status { get; set; }         // "On Time", "Delayed", "Cancelled", "Boarding"
    public string Gate { get; set; }           // e.g., "A12"
    public string Terminal { get; set; }       // e.g., "Terminal 1"
}

// === Gate Model (GATEINFO.Core/Models/Gate.cs) ===
public class Gate
{
    public string Airport { get; set; }        // IATA code
    public string GateNumber { get; set; }     // e.g., "A12"
    public string Terminal { get; set; }       // e.g., "Terminal 1"
    public string Status { get; set; }         // "Open", "Closed", "Boarding", "Maintenance"
    public string AssignedFlight { get; set; } // Flight number or null
    public string Airline { get; set; }        // Airline using this gate
    public string LastUpdated { get; set; }    // ISO 8601
}

// === Weather Model (WEATHER.Core/Models/AirportWeather.cs) ===
public class AirportWeather
{
    public string Airport { get; set; }        // IATA code
    public string Condition { get; set; }      // "Clear", "Cloudy", "Rain", "Snow", "Fog"
    public double TemperatureF { get; set; }   // Fahrenheit
    public double TemperatureC { get; set; }   // Celsius
    public string WindSpeed { get; set; }      // e.g., "15 mph NW"
    public string Visibility { get; set; }     // e.g., "10 miles"
    public int Humidity { get; set; }          // Percentage
    public string LastUpdated { get; set; }    // ISO 8601
}
```

### List of Tasks

```yaml
Task 1:
UPDATE .gitignore:
  - APPEND C#/.NET entries: bin/, obj/, *.dll, *.exe, *.pdb, .vs/, *.user, *.suo, packages/

Task 2:
CREATE flight-status solution and projects:
  - CREATE src/flight-status/src/ directory structure
  - RUN: dotnet new sln -n FlightStatus -o src/flight-status/src/
  - RUN: dotnet new webapi --use-controllers -n FLIGHTSTATUS.CLI -o src/flight-status/src/FLIGHTSTATUS.CLI
  - RUN: dotnet new classlib -n FLIGHTSTATUS.Core -o src/flight-status/src/FLIGHTSTATUS.Core
  - RUN: dotnet new classlib -n FLIGHTSTATUS.Services -o src/flight-status/src/FLIGHTSTATUS.Services
  - RUN: dotnet new xunit -n FLIGHTSTATUS.Tests -o src/flight-status/src/FLIGHTSTATUS.Tests
  - ADD all projects to solution
  - ADD project references:
    - CLI → Core, Services
    - Services → Core
    - Tests → Core, Services, CLI
  - ADD NuGet packages:
    - FLIGHTSTATUS.CLI: Swashbuckle.AspNetCore (v6.6.1+)
    - FLIGHTSTATUS.Tests: Microsoft.AspNetCore.Mvc.Testing, Moq

Task 3:
CREATE flight-status Core project files:
  - CREATE Models/Flight.cs (data model as defined above)
  - CREATE Interfaces/IFlightStatusService.cs (service interface)
  - REMOVE default Class1.cs

Task 4:
CREATE flight-status Services project:
  - CREATE FlightStatusService.cs implementing IFlightStatusService
  - CREATE Data/flights.json with stub data (3-5 airports, 15-20 flights)
  - CONFIGURE flights.json as CopyToOutputDirectory=PreserveNewest in .csproj
  - IMPLEMENT parameterized filtering (airport, flightNumber, time)
  - REMOVE default Class1.cs

Task 5:
CREATE flight-status CLI project (API entry point):
  - MODIFY Program.cs: register services (DI), configure Swagger, set port 5001
  - CREATE Controllers/FlightsController.cs with GET /api/flights endpoint
  - CONFIGURE appsettings.json with data file path
  - REMOVE template WeatherForecast files if generated

Task 6:
CREATE flight-status xUnit tests:
  - CREATE Services/FlightStatusServiceTests.cs (test filtering logic)
  - CREATE Controllers/FlightsControllerTests.cs (test HTTP responses with WebApplicationFactory)
  - VERIFY: dotnet test passes

Task 7:
CREATE flight-status Dockerfile:
  - Multi-stage build: mcr.microsoft.com/dotnet/sdk:8.0 (build) → mcr.microsoft.com/dotnet/aspnet:8.0 (runtime)
  - EXPOSE port 5001
  - SET ASPNETCORE_HTTP_PORTS=5001

Task 8:
CREATE gate-info microservice:
  - MIRROR flight-status structure exactly
  - REPLACE models: Gate instead of Flight
  - REPLACE endpoint: GET /api/gates?airport={code}&gateNumber={number}
  - CREATE Data/gates.json (3-5 airports, 10-15 gates each)
  - PORT: 5002
  - VERIFY: dotnet test passes

Task 9:
CREATE weather microservice:
  - MIRROR flight-status structure exactly
  - REPLACE models: AirportWeather instead of Flight
  - REPLACE endpoint: GET /api/weather?airport={code}
  - CREATE Data/weather.json (3-5 airports, one weather record each)
  - PORT: 5003
  - VERIFY: dotnet test passes
```

### Per-Task Pseudocode

```csharp
// === Program.cs (FLIGHTSTATUS.CLI) ===
var builder = WebApplication.CreateBuilder(args);

// Register services
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c => {
    c.SwaggerDoc("v1", new() { Title = "Flight Status API", Version = "v1" });
});

// Register our service as singleton (loads JSON once at startup)
builder.Services.AddSingleton<IFlightStatusService, FlightStatusService>();

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();
app.MapControllers();
app.Run();

// === FlightsController.cs ===
[ApiController]
[Route("api/[controller]")]
public class FlightsController : ControllerBase
{
    private readonly IFlightStatusService _service;

    public FlightsController(IFlightStatusService service) => _service = service;

    [HttpGet]
    public ActionResult<IEnumerable<Flight>> Get(
        [FromQuery] string? airport,
        [FromQuery] string? flightNumber,
        [FromQuery] string? time)
    {
        var results = _service.GetFlights(airport, flightNumber, time);
        return Ok(results); // Always 200, empty [] if no matches
    }
}

// === FlightStatusService.cs ===
public class FlightStatusService : IFlightStatusService
{
    private readonly List<Flight> _flights;

    public FlightStatusService()
    {
        // PATTERN: Load JSON at construction (singleton = once at startup)
        var json = File.ReadAllText("Data/flights.json");
        _flights = JsonSerializer.Deserialize<List<Flight>>(json,
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true }) ?? new();
    }

    public IEnumerable<Flight> GetFlights(string? airport, string? flightNumber, string? time)
    {
        var query = _flights.AsEnumerable();
        if (!string.IsNullOrEmpty(airport))
            query = query.Where(f => f.Airport.Equals(airport, StringComparison.OrdinalIgnoreCase));
        if (!string.IsNullOrEmpty(flightNumber))
            query = query.Where(f => f.FlightNumber == flightNumber);
        if (!string.IsNullOrEmpty(time))
            query = query.Where(f => f.DepartureTime.StartsWith(time)); // Prefix match on ISO date
        return query.ToList();
    }
}

// === Dockerfile ===
// FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
// WORKDIR /src
// COPY src/ .
// RUN dotnet restore FlightStatus.sln
// RUN dotnet publish FLIGHTSTATUS.CLI/FLIGHTSTATUS.CLI.csproj -c Release -o /app
//
// FROM mcr.microsoft.com/dotnet/aspnet:8.0
// WORKDIR /app
// COPY --from=build /app .
// ENV ASPNETCORE_HTTP_PORTS=5001
// EXPOSE 5001
// ENTRYPOINT ["dotnet", "FLIGHTSTATUS.CLI.dll"]
```

### Integration Points

```yaml
API/ROUTES:
  - flight-status: GET /api/flights?airport={code}&flightNumber={number}&time={time}
    port: 5001
  - gate-info: GET /api/gates?airport={code}&gateNumber={number}
    port: 5002
  - weather: GET /api/weather?airport={code}
    port: 5003

CONFIG:
  - Each service: appsettings.json for data file paths
  - Dockerfile: ASPNETCORE_HTTP_PORTS environment variable
  - JSON stub data files in Services/Data/ directory

DOCKER:
  - Base images: mcr.microsoft.com/dotnet/sdk:8.0 (build), mcr.microsoft.com/dotnet/aspnet:8.0 (runtime)
  - Multi-stage builds to minimize image size
  - JSON data files copied into runtime image
```

## Validation Loop

### Level 1: Syntax & Build

```bash
# Build each service (from respective src/ dirs)
dotnet build src/flight-status/src/FlightStatus.sln
dotnet build src/gate-info/src/GateInfo.sln
dotnet build src/weather/src/Weather.sln

# Expected: Build succeeded. 0 Error(s)
```

### Level 2: Tests

```bash
# Run tests for each service
dotnet test src/flight-status/src/FlightStatus.sln
dotnet test src/gate-info/src/GateInfo.sln
dotnet test src/weather/src/Weather.sln

# Expected: All tests pass
```

### Level 3: Docker

```bash
# Build Docker images
docker build -t flight-status -f src/flight-status/Dockerfile src/flight-status/
docker build -t gate-info -f src/gate-info/Dockerfile src/gate-info/
docker build -t weather -f src/weather/Dockerfile src/weather/

# Run and test
docker run -d -p 5001:5001 --name fs-test flight-status
curl http://localhost:5001/api/flights?airport=BDL
curl http://localhost:5001/swagger/v1/swagger.json
docker stop fs-test && docker rm fs-test
```

## Final Validation Checklist

- [ ] All three solutions build: `dotnet build`
- [ ] All tests pass: `dotnet test` for each solution
- [ ] Swagger UI accessible at `/swagger` for each service
- [ ] Query with valid airport returns filtered results
- [ ] Query with unknown airport returns HTTP 200 with `[]`
- [ ] Docker images build successfully
- [ ] Docker containers start and respond to HTTP requests
- [ ] .gitignore updated with C#/.NET entries
- [ ] JSON stub data covers 3-5 airports per service

## Task Breakdown

See: [docs/tasks/phase1-csharp-microservices.md](../tasks/phase1-csharp-microservices.md)

---

**PRP Confidence Score: 8/10**

High confidence due to well-established .NET 8 patterns and clear requirements. Minor risk around ensuring JSON data file copying works correctly in Docker multi-stage builds.
