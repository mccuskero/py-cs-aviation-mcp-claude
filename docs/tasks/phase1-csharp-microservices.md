# Task Breakdown: Phase 1 -- Stubbed C# Microservices

> **Source PRP**: [docs/prps/phase1-csharp-microservices.md](/docs/prps/phase1-csharp-microservices.md)
> **Generated**: 2026-02-09
> **Complexity**: Complex (9 implementation tasks, 3 microservices, multi-project .NET solutions)
> **Phase**: 1 of 3 (Aviation MCP Project)

---

## PRP Analysis Summary

- **Feature**: Three C# .NET 8 microservices (flight-status, gate-info, weather) providing parameterized stubbed aviation data via REST APIs
- **Pattern**: Controller -> Service -> Core layered architecture per microservice
- **Key Technical Requirements**: .NET 8, ASP.NET Core Controllers, Swagger/Swashbuckle, xUnit tests, Docker multi-stage builds, System.Text.Json for JSON stub loading
- **Validation Requirements**: All three solutions build, all tests pass, Swagger UI accessible, parameterized filtering works, Docker images build and run, empty results return HTTP 200 with `[]`

## Task Complexity Assessment

- **Overall Complexity**: Complex -- 9 PRP tasks expanding to 9 detailed implementation tasks across 3 phases
- **Integration Points**: Each microservice is independent; flight-status establishes the pattern that gate-info and weather replicate
- **Technical Challenges**:
  - .NET 8 port default change (80 -> 8080 in containers)
  - Swashbuckle not included by default in .NET 8
  - JSON data files must be copied into Docker container via CopyToOutputDirectory
  - System.Text.Json camelCase defaults must align with JSON stub files

## Critical Path Analysis

```
T-001 (.gitignore) ─────────────────────────────────────────────────┐
                                                                     │
T-002 (flight-status scaffold) ──> T-003 (Core) ──> T-004 (Services)│
                                                         │           │
                                                         v           │
                                            T-005 (CLI/Controller) ──┤
                                                         │           │
                                                         v           │
                                            T-006 (xUnit tests) ────┤
                                                         │           │
                                                         v           │
                                            T-007 (Dockerfile) ─────┤
                                                         │           │
                                                         v           │
                                            T-008 (gate-info) ──────┤
                                                         │           │
                                                         v           │
                                            T-009 (weather) ────────┘
```

- **Critical Path**: T-002 -> T-003 -> T-004 -> T-005 -> T-006 -> T-007 -> T-008 -> T-009
- **Parallelization Opportunity**: T-001 can be done in parallel with any task. T-008 and T-009 can be parallelized with each other once T-006 establishes the test pattern.
- **Bottleneck**: T-002 through T-006 are strictly sequential since each builds on the previous layer.

---

## Phase Organization

### Phase A: Foundation and Pattern Establishment (Tasks T-001 through T-007)
- **Objective**: Set up the project foundation and build the complete flight-status microservice as the reference pattern
- **Deliverables**: Updated .gitignore, fully functional flight-status service with tests and Docker
- **Milestone**: flight-status service passes all validation levels (build, test, Docker)

### Phase B: Pattern Replication (Tasks T-008 and T-009)
- **Objective**: Replicate the flight-status pattern for gate-info and weather microservices
- **Deliverables**: Two additional microservices, each with full test coverage and Docker support
- **Milestone**: All three services pass the Final Validation Checklist from the PRP

---

## Detailed Task Breakdown

---

### T-001: Update .gitignore with C#/.NET Entries

**Task ID**: T-001
**Task Name**: Update .gitignore with C#/.NET Entries
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase1-csharp-microservices.md](/docs/prps/phase1-csharp-microservices.md) -- Task 1

##### Feature Overview
The existing `.gitignore` only contains Python entries. Before any C# code is generated, the gitignore must be extended to prevent committing build artifacts, IDE files, and NuGet packages.

##### Task Purpose
**As a** developer
**I need** C#/.NET entries in .gitignore
**So that** build artifacts (bin/, obj/, *.dll, etc.) and IDE files (.vs/, *.user) are never committed to the repository

##### Dependencies
- **Prerequisite Tasks**: None
- **Parallel Tasks**: Can run in parallel with any other task
- **Integration Points**: None
- **Blocked By**: None

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When C# projects are built, the bin/ and obj/ directories shall be excluded from version control
- **REQ-2**: When Visual Studio or Rider opens the project, IDE-specific files shall be excluded from version control

##### Non-Functional Requirements
- **Performance**: N/A
- **Security**: Prevent accidental commit of sensitive build outputs

##### Technical Constraints
- **Technology Stack**: Git
- **Code Standards**: Append to existing file; do not remove Python entries

#### Implementation Details

##### Files to Modify/Create
```
.gitignore - MODIFY: Append C#/.NET entries after existing Python entries
```

##### Key Implementation Steps
1. **Read existing .gitignore** -> Confirm current Python entries
2. **Append C#/.NET section** with clear header comment -> Entries added
3. **Verify** no Python entries were removed -> Existing entries intact

##### Entries to Add
```gitignore
# C# / .NET
bin/
obj/
*.dll
*.exe
*.pdb
*.cache
.vs/
*.user
*.suo
*.nupkg
packages/
*.DotSettings.user
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: C# build artifacts excluded
  Given the .gitignore has been updated with C#/.NET entries
  When a developer runs "dotnet build" in any C# project
  Then the bin/ and obj/ directories are not tracked by git

Scenario 2: Existing Python entries preserved
  Given the .gitignore had Python entries before the update
  When the update is applied
  Then all original Python entries remain intact
```

##### Rule-Based Criteria (Checklist)
- [ ] .gitignore contains bin/, obj/, *.dll, *.exe, *.pdb entries
- [ ] .gitignore contains .vs/, *.user, *.suo entries
- [ ] .gitignore contains packages/ entry
- [ ] All pre-existing Python entries are preserved
- [ ] Entries are organized under a clear "C# / .NET" comment header

#### Validation & Quality Gates

##### Code Quality Checks
```bash
# Verify gitignore contains C# entries
grep -c "bin/" .gitignore
grep -c "obj/" .gitignore
grep -c "\.dll" .gitignore

# Verify Python entries still present
grep -c "__pycache__" .gitignore || grep -c ".pyc" .gitignore
```

##### Definition of Done
- [ ] .gitignore updated with all required C#/.NET entries
- [ ] Python entries preserved
- [ ] Changes committed

---

### T-002: Create flight-status Solution and Project Scaffolding

**Task ID**: T-002
**Task Name**: Create flight-status Solution and Project Scaffolding
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase1-csharp-microservices.md](/docs/prps/phase1-csharp-microservices.md) -- Task 2

##### Feature Overview
Scaffold the .NET 8 solution structure for the flight-status microservice. This is the pattern-setting service; its structure will be exactly replicated by gate-info and weather.

##### Task Purpose
**As a** developer
**I need** a properly scaffolded .NET 8 solution with four projects (CLI, Core, Services, Tests)
**So that** the layered Controller -> Service -> Core architecture is established with correct project references and NuGet dependencies

##### Dependencies
- **Prerequisite Tasks**: T-001 (recommended, not strictly blocking)
- **Parallel Tasks**: T-001
- **Integration Points**: None -- this is the foundation
- **Blocked By**: .NET 8 SDK must be installed

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When `dotnet build` is run on the solution, all four projects shall build successfully with zero errors
- **REQ-2**: When project references are inspected, CLI shall reference Core and Services, Services shall reference Core, Tests shall reference Core, Services, and CLI

##### Non-Functional Requirements
- **Compatibility**: .NET 8 (LTS)

##### Technical Constraints
- **Technology Stack**: .NET 8, ASP.NET Core with Controllers
- **Architecture Patterns**: Controller -> Service -> Core layering
- **Code Standards**: UPPERCASE project naming convention (FLIGHTSTATUS.CLI, FLIGHTSTATUS.Core, etc.)

#### Implementation Details

##### Files to Modify/Create
```
src/flight-status/src/
├── FlightStatus.sln                    - CREATE: Solution file
├── FLIGHTSTATUS.CLI/
│   └── FLIGHTSTATUS.CLI.csproj         - CREATE: Web API project
├── FLIGHTSTATUS.Core/
│   └── FLIGHTSTATUS.Core.csproj        - CREATE: Class library
├── FLIGHTSTATUS.Services/
│   └── FLIGHTSTATUS.Services.csproj    - CREATE: Class library
└── FLIGHTSTATUS.Tests/
    └── FLIGHTSTATUS.Tests.csproj       - CREATE: xUnit test project
```

##### Key Implementation Steps
1. **Create directory structure**: `mkdir -p src/flight-status/src/` -> Directory exists
2. **Scaffold solution**: `dotnet new sln -n FlightStatus -o src/flight-status/src/` -> Solution file created
3. **Scaffold CLI project**: `dotnet new webapi --use-controllers -n FLIGHTSTATUS.CLI -o src/flight-status/src/FLIGHTSTATUS.CLI` -> Web API project created
4. **Scaffold Core project**: `dotnet new classlib -n FLIGHTSTATUS.Core -o src/flight-status/src/FLIGHTSTATUS.Core` -> Class library created
5. **Scaffold Services project**: `dotnet new classlib -n FLIGHTSTATUS.Services -o src/flight-status/src/FLIGHTSTATUS.Services` -> Class library created
6. **Scaffold Tests project**: `dotnet new xunit -n FLIGHTSTATUS.Tests -o src/flight-status/src/FLIGHTSTATUS.Tests` -> Test project created
7. **Add all projects to solution**:
   ```bash
   cd src/flight-status/src/
   dotnet sln add FLIGHTSTATUS.CLI/FLIGHTSTATUS.CLI.csproj
   dotnet sln add FLIGHTSTATUS.Core/FLIGHTSTATUS.Core.csproj
   dotnet sln add FLIGHTSTATUS.Services/FLIGHTSTATUS.Services.csproj
   dotnet sln add FLIGHTSTATUS.Tests/FLIGHTSTATUS.Tests.csproj
   ```
8. **Add project references**:
   ```bash
   dotnet add FLIGHTSTATUS.CLI reference FLIGHTSTATUS.Core
   dotnet add FLIGHTSTATUS.CLI reference FLIGHTSTATUS.Services
   dotnet add FLIGHTSTATUS.Services reference FLIGHTSTATUS.Core
   dotnet add FLIGHTSTATUS.Tests reference FLIGHTSTATUS.Core
   dotnet add FLIGHTSTATUS.Tests reference FLIGHTSTATUS.Services
   dotnet add FLIGHTSTATUS.Tests reference FLIGHTSTATUS.CLI
   ```
9. **Add NuGet packages**:
   ```bash
   dotnet add FLIGHTSTATUS.CLI package Swashbuckle.AspNetCore --version 6.6.2
   dotnet add FLIGHTSTATUS.Tests package Microsoft.AspNetCore.Mvc.Testing
   dotnet add FLIGHTSTATUS.Tests package Moq
   ```
10. **Verify build**: `dotnet build FlightStatus.sln` -> Build succeeded, 0 errors

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Solution builds successfully
  Given the solution and all four projects have been scaffolded
  When "dotnet build FlightStatus.sln" is run from src/flight-status/src/
  Then the build succeeds with 0 errors

Scenario 2: Project references are correct
  Given the solution is scaffolded
  When the .csproj files are inspected
  Then FLIGHTSTATUS.CLI references Core and Services
  And FLIGHTSTATUS.Services references Core
  And FLIGHTSTATUS.Tests references Core, Services, and CLI

Scenario 3: NuGet packages are present
  Given the solution is scaffolded
  When FLIGHTSTATUS.CLI.csproj is inspected
  Then it contains a PackageReference for Swashbuckle.AspNetCore
  And FLIGHTSTATUS.Tests.csproj contains PackageReferences for Microsoft.AspNetCore.Mvc.Testing and Moq
```

##### Rule-Based Criteria (Checklist)
- [ ] Solution file FlightStatus.sln exists at src/flight-status/src/
- [ ] Four projects exist: CLI, Core, Services, Tests
- [ ] All four projects are included in the solution
- [ ] Project references follow the layered pattern (CLI->Core,Services; Services->Core; Tests->all)
- [ ] Swashbuckle.AspNetCore NuGet package added to CLI project
- [ ] Microsoft.AspNetCore.Mvc.Testing and Moq added to Tests project
- [ ] `dotnet build` succeeds with 0 errors
- [ ] Template-generated WeatherForecast files identified for removal in T-005

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/flight-status/src/
dotnet build FlightStatus.sln
# Expected: Build succeeded. 0 Error(s)

dotnet sln list
# Expected: All four .csproj files listed
```

##### Definition of Done
- [ ] Solution builds with zero errors
- [ ] All project references verified
- [ ] NuGet packages restored successfully

#### Resources & References

##### Documentation Links
- **Primary Docs**: https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-sln -- Solution management CLI
- **API Reference**: https://learn.microsoft.com/en-us/aspnet/core/web-api/?view=aspnetcore-8.0 -- Controller-based API

##### Implementation Notes
- The `--use-controllers` flag on `dotnet new webapi` is essential; without it, .NET 8 defaults to Minimal APIs
- The webapi template may generate WeatherForecast sample files; these will be removed in T-005
- Swashbuckle is NOT included by default in .NET 8 templates and must be added manually

---

### T-003: Create flight-status Core Project Files (Models and Interfaces)

**Task ID**: T-003
**Task Name**: Create flight-status Core Project Files (Models and Interfaces)
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase1-csharp-microservices.md](/docs/prps/phase1-csharp-microservices.md) -- Task 3

##### Feature Overview
Create the domain model and service interface for the flight-status microservice. The Core project defines the data contract used by all other layers.

##### Task Purpose
**As a** developer
**I need** the Flight data model and IFlightStatusService interface defined in the Core project
**So that** the Services and CLI projects can implement and consume a well-defined contract

##### Dependencies
- **Prerequisite Tasks**: T-002 (solution scaffolding must exist)
- **Parallel Tasks**: None
- **Integration Points**: Model definition used by Services (T-004) and CLI (T-005)
- **Blocked By**: None

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: The Flight model shall contain all fields defined in the PRP data model specification
- **REQ-2**: The IFlightStatusService interface shall define a method for querying flights with optional parameters

##### Technical Constraints
- **Technology Stack**: .NET 8, C#
- **Architecture Patterns**: Core project contains only models and interfaces -- no implementation logic
- **Code Standards**: Properties use PascalCase; JSON serialization will use camelCase by default in ASP.NET Core

#### Implementation Details

##### Files to Modify/Create
```
src/flight-status/src/FLIGHTSTATUS.Core/
├── Models/
│   └── Flight.cs                      - CREATE: Flight data model
├── Interfaces/
│   └── IFlightStatusService.cs        - CREATE: Service interface
└── Class1.cs                          - DELETE: Remove template default
```

##### Key Implementation Steps
1. **Create Models directory** -> Directory exists
2. **Create Flight.cs** with all PRP-defined properties -> Model class created
3. **Create Interfaces directory** -> Directory exists
4. **Create IFlightStatusService.cs** -> Interface defined
5. **Delete Class1.cs** -> Template default removed
6. **Verify build** -> Compiles successfully

##### Code Patterns to Follow

**Flight.cs**:
```csharp
namespace FLIGHTSTATUS.Core.Models;

public class Flight
{
    public string Airport { get; set; } = string.Empty;       // IATA code: "BDL", "JFK"
    public string FlightNumber { get; set; } = string.Empty;  // e.g., "1234"
    public string Airline { get; set; } = string.Empty;       // e.g., "Delta"
    public string Origin { get; set; } = string.Empty;        // IATA code
    public string Destination { get; set; } = string.Empty;   // IATA code
    public string DepartureTime { get; set; } = string.Empty; // ISO 8601
    public string ArrivalTime { get; set; } = string.Empty;   // ISO 8601
    public string Status { get; set; } = string.Empty;        // "On Time", "Delayed", etc.
    public string Gate { get; set; } = string.Empty;          // e.g., "A12"
    public string Terminal { get; set; } = string.Empty;      // e.g., "Terminal 1"
}
```

**IFlightStatusService.cs**:
```csharp
using FLIGHTSTATUS.Core.Models;

namespace FLIGHTSTATUS.Core.Interfaces;

public interface IFlightStatusService
{
    IEnumerable<Flight> GetFlights(string? airport, string? flightNumber, string? time);
}
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Flight model has all required properties
  Given the Flight.cs model is created
  When its properties are inspected
  Then it contains: Airport, FlightNumber, Airline, Origin, Destination, DepartureTime, ArrivalTime, Status, Gate, Terminal

Scenario 2: Interface defines query method
  Given IFlightStatusService.cs is created
  When its methods are inspected
  Then it defines GetFlights(string? airport, string? flightNumber, string? time) returning IEnumerable<Flight>

Scenario 3: Template default removed
  Given Class1.cs existed from scaffolding
  When the Core project is finalized
  Then Class1.cs no longer exists
```

##### Rule-Based Criteria (Checklist)
- [ ] Flight.cs exists at FLIGHTSTATUS.Core/Models/Flight.cs
- [ ] Flight model has all 10 properties from PRP specification
- [ ] All string properties initialized with `string.Empty` to avoid null warnings
- [ ] IFlightStatusService.cs exists at FLIGHTSTATUS.Core/Interfaces/IFlightStatusService.cs
- [ ] Interface method parameters are all nullable (string?)
- [ ] Class1.cs is deleted
- [ ] `dotnet build` succeeds

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/flight-status/src/
dotnet build FlightStatus.sln
# Expected: Build succeeded. 0 Error(s)

# Verify Class1.cs removed
test ! -f FLIGHTSTATUS.Core/Class1.cs && echo "PASS: Class1.cs removed"
```

##### Definition of Done
- [ ] Model and interface files created
- [ ] Template default removed
- [ ] Solution builds cleanly

---

### T-004: Create flight-status Services Project (Business Logic and Stub Data)

**Task ID**: T-004
**Task Name**: Create flight-status Services Project (Business Logic and Stub Data)
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase1-csharp-microservices.md](/docs/prps/phase1-csharp-microservices.md) -- Task 4

##### Feature Overview
Implement the service layer that loads JSON stub data and provides parameterized filtering. This is the core business logic of the flight-status microservice.

##### Task Purpose
**As a** developer
**I need** a FlightStatusService that loads flights from JSON and filters by airport, flightNumber, and time parameters
**So that** the REST API can serve parameterized stub data with real filtering logic

##### Dependencies
- **Prerequisite Tasks**: T-003 (Core models and interface must exist)
- **Parallel Tasks**: None
- **Integration Points**: Implements IFlightStatusService from Core; consumed by Controller in T-005
- **Blocked By**: None

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When the service is constructed, it shall load all flight data from Data/flights.json
- **REQ-2**: When GetFlights is called with an airport parameter, the service shall return only flights matching that IATA code (case-insensitive)
- **REQ-3**: When GetFlights is called with a flightNumber parameter, the service shall return only flights with that exact flight number
- **REQ-4**: When GetFlights is called with a time parameter, the service shall return flights whose DepartureTime starts with the given prefix (ISO 8601 prefix match)
- **REQ-5**: When GetFlights is called with no parameters, the service shall return all flights
- **REQ-6**: When GetFlights matches no flights, the service shall return an empty collection (not null)

##### Technical Constraints
- **Technology Stack**: System.Text.Json for deserialization
- **Architecture Patterns**: Singleton service (loads JSON once at startup)
- **Code Standards**: PropertyNameCaseInsensitive = true for JSON deserialization

#### Implementation Details

##### Files to Modify/Create
```
src/flight-status/src/FLIGHTSTATUS.Services/
├── FlightStatusService.cs             - CREATE: Service implementation
├── Data/
│   └── flights.json                   - CREATE: Stub data (3-5 airports, 15-20 flights)
├── FLIGHTSTATUS.Services.csproj       - MODIFY: Add CopyToOutputDirectory for flights.json
└── Class1.cs                          - DELETE: Remove template default
```

##### Key Implementation Steps
1. **Create FlightStatusService.cs** implementing IFlightStatusService -> Service class created
2. **Create Data directory** -> Directory exists
3. **Create flights.json** with 15-20 flights across 3-5 airports -> Stub data created
4. **Modify .csproj** to set CopyToOutputDirectory=PreserveNewest for Data/** -> JSON copied on build
5. **Delete Class1.cs** -> Template default removed
6. **Verify build and data loading** -> Service instantiates and loads data

##### Code Patterns to Follow

**FlightStatusService.cs** (from PRP pseudocode):
```csharp
using System.Text.Json;
using FLIGHTSTATUS.Core.Interfaces;
using FLIGHTSTATUS.Core.Models;

namespace FLIGHTSTATUS.Services;

public class FlightStatusService : IFlightStatusService
{
    private readonly List<Flight> _flights;

    public FlightStatusService()
    {
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
            query = query.Where(f => f.DepartureTime.StartsWith(time));
        return query.ToList();
    }
}
```

**.csproj addition**:
```xml
<ItemGroup>
  <None Update="Data\flights.json">
    <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
  </None>
</ItemGroup>
```

**flights.json** (sample structure -- create 15-20 records across BDL, JFK, LAX, ORD, ATL):
```json
[
  {
    "airport": "BDL",
    "flightNumber": "DL1234",
    "airline": "Delta",
    "origin": "BDL",
    "destination": "ATL",
    "departureTime": "2026-02-09T14:30:00Z",
    "arrivalTime": "2026-02-09T17:45:00Z",
    "status": "On Time",
    "gate": "A12",
    "terminal": "Terminal 1"
  }
]
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Load all flights
  Given the service has loaded flights.json with 15-20 records
  When GetFlights is called with no parameters (all null)
  Then all flights are returned

Scenario 2: Filter by airport (case-insensitive)
  Given flights exist for airports BDL and JFK
  When GetFlights is called with airport="bdl"
  Then only BDL flights are returned

Scenario 3: Filter by flight number
  Given a flight with number "DL1234" exists
  When GetFlights is called with flightNumber="DL1234"
  Then only that specific flight is returned

Scenario 4: Filter by time prefix
  Given flights exist with various departure times
  When GetFlights is called with time="2026-02-09"
  Then only flights departing on that date are returned

Scenario 5: No matches returns empty collection
  Given no flights exist for airport "ZZZ"
  When GetFlights is called with airport="ZZZ"
  Then an empty collection is returned (not null)

Scenario 6: Multiple filters combine with AND logic
  Given flights exist for BDL with various flight numbers
  When GetFlights is called with airport="BDL" and flightNumber="DL1234"
  Then only the BDL flight with number DL1234 is returned
```

##### Rule-Based Criteria (Checklist)
- [ ] FlightStatusService.cs implements IFlightStatusService
- [ ] JSON deserialization uses PropertyNameCaseInsensitive = true
- [ ] flights.json contains 15-20 flight records across 3-5 airports (BDL, JFK, LAX, ORD, ATL)
- [ ] flights.json uses camelCase property names
- [ ] .csproj configured with CopyToOutputDirectory=PreserveNewest for Data/flights.json
- [ ] Airport filtering is case-insensitive
- [ ] Time filtering uses prefix matching on ISO 8601 strings
- [ ] Empty results return empty collection, not null
- [ ] Class1.cs is deleted
- [ ] `dotnet build` succeeds

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/flight-status/src/
dotnet build FlightStatus.sln
# Expected: Build succeeded. 0 Error(s)

# Verify JSON file exists and is valid
cat FLIGHTSTATUS.Services/Data/flights.json | python3 -m json.tool > /dev/null
# Expected: Valid JSON

# Verify Class1.cs removed
test ! -f FLIGHTSTATUS.Services/Class1.cs && echo "PASS: Class1.cs removed"
```

##### Definition of Done
- [ ] Service implementation complete with all filtering logic
- [ ] Stub data file created with sufficient test data
- [ ] CopyToOutputDirectory configured
- [ ] Solution builds cleanly

#### Implementation Notes
- **GOTCHA**: System.Text.Json defaults to camelCase in ASP.NET Core. The flights.json must use camelCase keys to match, OR PropertyNameCaseInsensitive must be true (which is the approach used here).
- **GOTCHA**: The `File.ReadAllText("Data/flights.json")` path is relative to the working directory. In Docker, this will be the WORKDIR. The CopyToOutputDirectory setting ensures the file is alongside the DLL.

---

### T-005: Create flight-status CLI Project (API Entry Point and Controller)

**Task ID**: T-005
**Task Name**: Create flight-status CLI Project (API Entry Point and Controller)
**Priority**: Critical

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase1-csharp-microservices.md](/docs/prps/phase1-csharp-microservices.md) -- Task 5

##### Feature Overview
Configure the ASP.NET Core entry point with DI registration, Swagger setup, and the FlightsController providing the REST API endpoint.

##### Task Purpose
**As a** developer
**I need** a properly configured ASP.NET Core application with Swagger and a FlightsController
**So that** the flight-status service is accessible via REST API at port 5001 with interactive documentation

##### Dependencies
- **Prerequisite Tasks**: T-004 (Services project must exist for DI registration)
- **Parallel Tasks**: None
- **Integration Points**: Consumes FlightStatusService via DI; exposes REST endpoint for Phase 2 Python MCP server
- **Blocked By**: None

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When the application starts, it shall listen on port 5001
- **REQ-2**: When `/swagger` is accessed, the Swagger UI shall be displayed
- **REQ-3**: When `GET /api/flights` is called with optional query parameters, the controller shall return filtered results as JSON
- **REQ-4**: When no flights match the query, the controller shall return HTTP 200 with an empty array `[]`

##### Technical Constraints
- **Technology Stack**: ASP.NET Core 8, Swashbuckle
- **Architecture Patterns**: [ApiController] attribute, constructor injection
- **Code Standards**: Route template `api/[controller]`; action returns `ActionResult<IEnumerable<Flight>>`

#### Implementation Details

##### Files to Modify/Create
```
src/flight-status/src/FLIGHTSTATUS.CLI/
├── Program.cs                         - MODIFY: Configure DI, Swagger, port 5001
├── Controllers/
│   └── FlightsController.cs           - CREATE: REST endpoint
├── appsettings.json                   - MODIFY: Review/update settings
└── [WeatherForecast files]            - DELETE: Remove template defaults if present
```

##### Key Implementation Steps
1. **Remove template-generated WeatherForecast files** (WeatherForecast.cs, Controllers/WeatherForecastController.cs if present) -> Template defaults removed
2. **Modify Program.cs**: Register DI services, configure Swagger, set port 5001 -> Application configured
3. **Create Controllers directory** (if not exists) -> Directory exists
4. **Create FlightsController.cs** with GET /api/flights endpoint -> Controller created
5. **Verify application starts** and Swagger is accessible -> Service running on port 5001

##### Code Patterns to Follow

**Program.cs** (from PRP pseudocode):
```csharp
using FLIGHTSTATUS.Core.Interfaces;
using FLIGHTSTATUS.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new() { Title = "Flight Status API", Version = "v1" });
});

// Register service as singleton (loads JSON once at startup)
builder.Services.AddSingleton<IFlightStatusService, FlightStatusService>();

// Set port
builder.WebHost.UseUrls("http://0.0.0.0:5001");

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();
app.MapControllers();
app.Run();
```

**FlightsController.cs** (from PRP pseudocode):
```csharp
using Microsoft.AspNetCore.Mvc;
using FLIGHTSTATUS.Core.Interfaces;
using FLIGHTSTATUS.Core.Models;

namespace FLIGHTSTATUS.CLI.Controllers;

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
```

##### API Specifications
```yaml
Method: GET
Path: /api/flights
Headers: Accept: application/json
Query Parameters:
  - airport: string (optional) - IATA airport code, case-insensitive
  - flightNumber: string (optional) - Flight number, exact match
  - time: string (optional) - ISO 8601 date/time prefix
Response:
  - status: 200
  - body: Flight[] (may be empty [])
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Service starts on port 5001
  Given the application is configured
  When it is started with "dotnet run"
  Then it listens on port 5001

Scenario 2: Swagger UI accessible
  Given the service is running
  When a browser navigates to http://localhost:5001/swagger
  Then the Swagger UI is displayed with the Flight Status API documentation

Scenario 3: Query returns filtered results
  Given the service is running with stub data
  When GET /api/flights?airport=BDL is called
  Then HTTP 200 is returned with a JSON array of BDL flights

Scenario 4: Empty result returns 200 with empty array
  Given the service is running
  When GET /api/flights?airport=ZZZ is called (no matching flights)
  Then HTTP 200 is returned with an empty JSON array []

Scenario 5: No parameters returns all flights
  Given the service is running
  When GET /api/flights is called with no query parameters
  Then HTTP 200 is returned with all flights from the stub data
```

##### Rule-Based Criteria (Checklist)
- [ ] Program.cs registers IFlightStatusService as singleton
- [ ] Program.cs configures Swagger with title "Flight Status API"
- [ ] Application listens on port 5001
- [ ] FlightsController uses [ApiController] attribute
- [ ] FlightsController route is "api/[controller]"
- [ ] GET endpoint accepts optional airport, flightNumber, time parameters
- [ ] All responses return HTTP 200 (including empty results)
- [ ] Template-generated WeatherForecast files removed
- [ ] `dotnet run` starts successfully and Swagger is accessible

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/flight-status/src/FLIGHTSTATUS.CLI/
dotnet run &
sleep 3

# Test Swagger
curl -s http://localhost:5001/swagger/v1/swagger.json | python3 -m json.tool > /dev/null
echo "Swagger: OK"

# Test endpoint with data
curl -s http://localhost:5001/api/flights?airport=BDL
echo ""

# Test empty result
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/api/flights?airport=ZZZ
# Expected: 200

kill %1
```

##### Definition of Done
- [ ] Application starts on port 5001
- [ ] Swagger UI accessible at /swagger
- [ ] GET /api/flights returns filtered results
- [ ] Empty results return HTTP 200 with []
- [ ] Template defaults removed

---

### T-006: Create flight-status xUnit Tests

**Task ID**: T-006
**Task Name**: Create flight-status xUnit Tests
**Priority**: High

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase1-csharp-microservices.md](/docs/prps/phase1-csharp-microservices.md) -- Task 6

##### Feature Overview
Create comprehensive xUnit tests for both the service layer (filtering logic) and controller layer (HTTP responses). These test patterns will be replicated for gate-info and weather.

##### Task Purpose
**As a** developer
**I need** xUnit tests covering service filtering logic and controller HTTP behavior
**So that** the flight-status microservice has verified correctness and the test pattern is established for replication

##### Dependencies
- **Prerequisite Tasks**: T-005 (Controller must exist for controller tests)
- **Parallel Tasks**: None
- **Integration Points**: Tests reference Core, Services, and CLI projects
- **Blocked By**: None

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: Service tests shall verify filtering by airport, flightNumber, and time parameters
- **REQ-2**: Service tests shall verify empty result behavior (returns empty collection)
- **REQ-3**: Controller tests shall verify HTTP 200 responses with filtered data
- **REQ-4**: Controller tests shall verify HTTP 200 with empty array for no-match queries

##### Technical Constraints
- **Technology Stack**: xUnit, Moq, Microsoft.AspNetCore.Mvc.Testing (WebApplicationFactory)
- **Code Standards**: Test method naming: `MethodName_Scenario_ExpectedResult`

#### Implementation Details

##### Files to Modify/Create
```
src/flight-status/src/FLIGHTSTATUS.Tests/
├── Services/
│   └── FlightStatusServiceTests.cs    - CREATE: Service layer tests
└── Controllers/
    └── FlightsControllerTests.cs      - CREATE: Controller/HTTP tests
```

##### Key Implementation Steps
1. **Create Services directory** -> Directory exists
2. **Create FlightStatusServiceTests.cs** with tests for all filtering scenarios -> Service tests created
3. **Create Controllers directory** -> Directory exists
4. **Create FlightsControllerTests.cs** using WebApplicationFactory or Moq -> Controller tests created
5. **Run all tests**: `dotnet test` -> All tests pass

##### Test Scenarios for FlightStatusServiceTests

```csharp
// Service Tests - test the filtering logic directly
[Fact] GetFlights_NoFilters_ReturnsAllFlights()
[Fact] GetFlights_FilterByAirport_ReturnsMatchingFlights()
[Fact] GetFlights_FilterByAirportCaseInsensitive_ReturnsMatchingFlights()
[Fact] GetFlights_FilterByFlightNumber_ReturnsMatchingFlight()
[Fact] GetFlights_FilterByTime_ReturnsMatchingFlights()
[Fact] GetFlights_FilterByMultipleParams_ReturnsCombinedFilter()
[Fact] GetFlights_NoMatches_ReturnsEmptyCollection()
```

##### Test Scenarios for FlightsControllerTests

```csharp
// Controller Tests - test HTTP responses using WebApplicationFactory or mock service
[Fact] Get_NoParams_Returns200WithFlights()
[Fact] Get_WithAirport_Returns200WithFilteredFlights()
[Fact] Get_NoMatches_Returns200WithEmptyArray()
[Fact] Get_SwaggerEndpoint_Returns200()
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: All tests pass
  Given all test files are created
  When "dotnet test" is run on the solution
  Then all tests pass with 0 failures

Scenario 2: Service filtering logic verified
  Given FlightStatusServiceTests exist
  When service tests are executed
  Then airport filtering, flight number filtering, time filtering, and empty result tests all pass

Scenario 3: Controller HTTP responses verified
  Given FlightsControllerTests exist
  When controller tests are executed
  Then HTTP 200 response tests pass for both populated and empty results
```

##### Rule-Based Criteria (Checklist)
- [ ] FlightStatusServiceTests.cs exists with at least 5 test methods
- [ ] FlightsControllerTests.cs exists with at least 3 test methods
- [ ] Tests cover: all-flights, filter-by-airport, filter-by-flightNumber, filter-by-time, empty-results
- [ ] Controller tests verify HTTP status codes
- [ ] `dotnet test` passes with 0 failures
- [ ] Test method names follow MethodName_Scenario_ExpectedResult convention

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/flight-status/src/
dotnet test FlightStatus.sln --verbosity normal
# Expected: All tests passed. 0 failed.
```

##### Definition of Done
- [ ] All service-layer tests pass
- [ ] All controller-layer tests pass
- [ ] Minimum 8 total tests across both test files
- [ ] `dotnet test` exits with code 0

---

### T-007: Create flight-status Dockerfile

**Task ID**: T-007
**Task Name**: Create flight-status Dockerfile
**Priority**: High

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase1-csharp-microservices.md](/docs/prps/phase1-csharp-microservices.md) -- Task 7

##### Feature Overview
Create a multi-stage Docker build for the flight-status microservice. This Dockerfile pattern will be replicated for gate-info and weather.

##### Task Purpose
**As a** developer
**I need** a multi-stage Dockerfile that builds and runs the flight-status service in a container
**So that** the service can be deployed independently and is ready for Docker Compose orchestration in Phase 3

##### Dependencies
- **Prerequisite Tasks**: T-005 (CLI project must be complete and runnable)
- **Parallel Tasks**: T-006 (tests are independent of Docker)
- **Integration Points**: Will be used by docker-compose.yml in Phase 3; JSON data files must be copied into image
- **Blocked By**: None

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When `docker build` is run, the image shall build successfully using multi-stage build
- **REQ-2**: When the container starts, the service shall listen on port 5001
- **REQ-3**: When the container is running, the flights.json data file shall be accessible to the service

##### Technical Constraints
- **Technology Stack**: Docker, .NET 8 SDK (build stage), .NET 8 ASP.NET runtime (runtime stage)
- **Code Standards**: Multi-stage build to minimize image size
- **CRITICAL**: .NET 8 changed default port from 80 to 8080 in containers; must set ASPNETCORE_HTTP_PORTS explicitly

#### Implementation Details

##### Files to Modify/Create
```
src/flight-status/
└── Dockerfile                         - CREATE: Multi-stage Docker build
```

##### Key Implementation Steps
1. **Create Dockerfile** at src/flight-status/Dockerfile -> Dockerfile created
2. **Build image**: `docker build -t flight-status -f src/flight-status/Dockerfile src/flight-status/` -> Image builds successfully
3. **Run container**: `docker run -d -p 5001:5001 --name fs-test flight-status` -> Container starts
4. **Test endpoint**: `curl http://localhost:5001/api/flights?airport=BDL` -> Returns data
5. **Test Swagger**: `curl http://localhost:5001/swagger/v1/swagger.json` -> Returns Swagger spec
6. **Cleanup**: `docker stop fs-test && docker rm fs-test` -> Container removed

##### Code Patterns to Follow

**Dockerfile** (from PRP pseudocode):
```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY src/ .
RUN dotnet restore FlightStatus.sln
RUN dotnet publish FLIGHTSTATUS.CLI/FLIGHTSTATUS.CLI.csproj -c Release -o /app

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app .
ENV ASPNETCORE_HTTP_PORTS=5001
EXPOSE 5001
ENTRYPOINT ["dotnet", "FLIGHTSTATUS.CLI.dll"]
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Docker image builds successfully
  Given the Dockerfile exists and the flight-status project builds
  When "docker build -t flight-status -f src/flight-status/Dockerfile src/flight-status/" is run
  Then the image builds successfully with no errors

Scenario 2: Container starts and serves API
  Given the Docker image is built
  When a container is started with port 5001 mapped
  Then the service responds to HTTP requests on port 5001

Scenario 3: Swagger accessible in container
  Given the container is running
  When http://localhost:5001/swagger/v1/swagger.json is requested
  Then a valid Swagger specification is returned

Scenario 4: JSON data available in container
  Given the container is running
  When GET /api/flights?airport=BDL is called
  Then filtered flight data is returned (not an error about missing data file)
```

##### Rule-Based Criteria (Checklist)
- [ ] Dockerfile exists at src/flight-status/Dockerfile
- [ ] Uses multi-stage build (sdk:8.0 for build, aspnet:8.0 for runtime)
- [ ] ASPNETCORE_HTTP_PORTS set to 5001
- [ ] EXPOSE 5001 declared
- [ ] flights.json is included in the published output (via CopyToOutputDirectory)
- [ ] `docker build` succeeds
- [ ] Container starts and responds to requests
- [ ] Swagger endpoint accessible in container

#### Validation & Quality Gates

##### Code Quality Checks
```bash
# Build image
docker build -t flight-status -f src/flight-status/Dockerfile src/flight-status/

# Run container
docker run -d -p 5001:5001 --name fs-test flight-status
sleep 3

# Test API
curl -s http://localhost:5001/api/flights?airport=BDL
curl -s http://localhost:5001/swagger/v1/swagger.json | python3 -m json.tool > /dev/null
echo "Docker validation: OK"

# Cleanup
docker stop fs-test && docker rm fs-test
```

##### Definition of Done
- [ ] Docker image builds successfully
- [ ] Container starts and serves API on port 5001
- [ ] API returns stub data from within container
- [ ] Swagger accessible within container

#### Implementation Notes
- **CRITICAL**: .NET 8 changed the default container port from 80 to 8080. The `ENV ASPNETCORE_HTTP_PORTS=5001` line is essential.
- **GOTCHA**: The COPY context is `src/flight-status/`, so the Dockerfile's `COPY src/ .` copies from `src/flight-status/src/` into the build container. Ensure the Dockerfile path and build context are correct.
- **GOTCHA**: The `dotnet publish` command copies files marked with CopyToOutputDirectory, which includes flights.json. No separate COPY step is needed for the data file.

---

### T-008: Create gate-info Microservice (Full Replication)

**Task ID**: T-008
**Task Name**: Create gate-info Microservice (Full Replication of flight-status Pattern)
**Priority**: High

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase1-csharp-microservices.md](/docs/prps/phase1-csharp-microservices.md) -- Task 8

##### Feature Overview
Create the gate-info microservice by replicating the exact structure of flight-status, replacing the domain model, endpoint, and stub data.

##### Task Purpose
**As a** developer
**I need** a gate-info microservice with the same layered architecture as flight-status
**So that** gate information is available via REST API for the Python MCP server in Phase 2

##### Dependencies
- **Prerequisite Tasks**: T-006 (flight-status must be complete including tests as the reference pattern)
- **Parallel Tasks**: T-009 (weather can be built in parallel with gate-info)
- **Integration Points**: Will be called by Python MCP server in Phase 2 at port 5002
- **Blocked By**: None

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When the service starts, it shall listen on port 5002
- **REQ-2**: When `GET /api/gates` is called with optional airport and gateNumber parameters, the controller shall return filtered gate data
- **REQ-3**: When no gates match the query, the controller shall return HTTP 200 with empty array `[]`
- **REQ-4**: The Swagger UI shall be accessible at `/swagger`

##### Technical Constraints
- **Technology Stack**: .NET 8, ASP.NET Core Controllers, Swashbuckle, xUnit
- **Architecture Patterns**: Identical layered structure to flight-status: CLI -> Services -> Core
- **Naming Convention**: GATEINFO.CLI, GATEINFO.Core, GATEINFO.Services, GATEINFO.Tests

#### Implementation Details

##### Files to Modify/Create
```
src/gate-info/
├── Dockerfile
└── src/
    ├── GateInfo.sln
    ├── GATEINFO.CLI/
    │   ├── GATEINFO.CLI.csproj
    │   ├── Program.cs                 - Swagger: "Gate Info API", port 5002
    │   ├── Controllers/
    │   │   └── GatesController.cs     - GET /api/gates?airport={code}&gateNumber={number}
    │   └── appsettings.json
    ├── GATEINFO.Core/
    │   ├── GATEINFO.Core.csproj
    │   ├── Models/
    │   │   └── Gate.cs                - Gate data model (7 properties)
    │   └── Interfaces/
    │       └── IGateInfoService.cs
    ├── GATEINFO.Services/
    │   ├── GATEINFO.Services.csproj
    │   ├── GateInfoService.cs         - JSON loading + filtering
    │   └── Data/
    │       └── gates.json             - 3-5 airports, 10-15 gates each
    └── GATEINFO.Tests/
        ├── GATEINFO.Tests.csproj
        ├── Services/
        │   └── GateInfoServiceTests.cs
        └── Controllers/
            └── GatesControllerTests.cs
```

##### Key Implementation Steps
1. **Scaffold solution and projects** (mirror T-002 with GATEINFO naming) -> Solution created
2. **Create Gate model** with properties: Airport, GateNumber, Terminal, Status, AssignedFlight, Airline, LastUpdated -> Model created
3. **Create IGateInfoService interface** with `GetGates(string? airport, string? gateNumber)` -> Interface created
4. **Create GateInfoService** loading gates.json with airport and gateNumber filtering -> Service created
5. **Create gates.json** with 10-15 gates per airport across 3-5 airports -> Stub data created
6. **Configure Program.cs** with DI, Swagger ("Gate Info API"), port 5002 -> Application configured
7. **Create GatesController** with GET /api/gates endpoint -> Controller created
8. **Create xUnit tests** for service and controller layers -> Tests created
9. **Create Dockerfile** (mirror T-007 with port 5002) -> Dockerfile created
10. **Verify**: `dotnet test`, `dotnet run`, Docker build -> All pass

##### Data Model

```csharp
// GATEINFO.Core/Models/Gate.cs
public class Gate
{
    public string Airport { get; set; } = string.Empty;
    public string GateNumber { get; set; } = string.Empty;
    public string Terminal { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;         // "Open", "Closed", "Boarding", "Maintenance"
    public string AssignedFlight { get; set; } = string.Empty;
    public string Airline { get; set; } = string.Empty;
    public string LastUpdated { get; set; } = string.Empty;
}
```

##### API Specifications
```yaml
Method: GET
Path: /api/gates
Headers: Accept: application/json
Query Parameters:
  - airport: string (optional) - IATA airport code, case-insensitive
  - gateNumber: string (optional) - Gate number, exact match
Response:
  - status: 200
  - body: Gate[] (may be empty [])
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Solution builds
  Given the gate-info solution is scaffolded
  When "dotnet build GateInfo.sln" is run
  Then the build succeeds with 0 errors

Scenario 2: Service starts on port 5002
  Given the application is configured
  When it is started with "dotnet run"
  Then it listens on port 5002

Scenario 3: Filter by airport
  Given the service is running with stub data
  When GET /api/gates?airport=BDL is called
  Then only BDL gates are returned with HTTP 200

Scenario 4: Filter by gate number
  Given the service is running
  When GET /api/gates?gateNumber=A12 is called
  Then only gates with number A12 are returned

Scenario 5: All tests pass
  Given all test files are created
  When "dotnet test" is run
  Then all tests pass with 0 failures

Scenario 6: Docker works
  Given the Dockerfile exists
  When the image is built and container started
  Then the service responds on port 5002
```

##### Rule-Based Criteria (Checklist)
- [ ] Solution GateInfo.sln builds with 0 errors
- [ ] Gate model has all 7 properties from PRP specification
- [ ] gates.json contains 10-15 gates per airport across 3-5 airports
- [ ] gates.json uses camelCase property names
- [ ] Service filters by airport (case-insensitive) and gateNumber
- [ ] Controller returns HTTP 200 for all cases (including empty results)
- [ ] Swagger UI accessible at /swagger with title "Gate Info API"
- [ ] Application listens on port 5002
- [ ] All xUnit tests pass
- [ ] Dockerfile builds and container runs successfully
- [ ] Project structure mirrors flight-status exactly

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/gate-info/src/
dotnet build GateInfo.sln
dotnet test GateInfo.sln --verbosity normal
# Expected: Build succeeded. All tests passed.

# Docker validation
docker build -t gate-info -f src/gate-info/Dockerfile src/gate-info/
docker run -d -p 5002:5002 --name gi-test gate-info
sleep 3
curl -s http://localhost:5002/api/gates?airport=BDL
docker stop gi-test && docker rm gi-test
```

##### Definition of Done
- [ ] Solution builds with 0 errors
- [ ] All tests pass
- [ ] Swagger accessible on port 5002
- [ ] Docker image builds and container runs
- [ ] Structure mirrors flight-status

#### Implementation Notes
- **PATTERN**: Follow the exact same layering, naming conventions, and code patterns established by flight-status (T-002 through T-007). The only differences are: model (Gate vs Flight), endpoint path (/api/gates vs /api/flights), query parameters (airport + gateNumber), port (5002), and stub data content.
- **REFERENCE**: Use `src/flight-status/` as the complete reference implementation to replicate from.

---

### T-009: Create weather Microservice (Full Replication)

**Task ID**: T-009
**Task Name**: Create weather Microservice (Full Replication of flight-status Pattern)
**Priority**: High

#### Context & Background

##### Source PRP Document
**Reference**: [docs/prps/phase1-csharp-microservices.md](/docs/prps/phase1-csharp-microservices.md) -- Task 9

##### Feature Overview
Create the weather microservice by replicating the exact structure of flight-status, replacing the domain model, endpoint, and stub data. This is the simplest of the three services (single query parameter, one record per airport).

##### Task Purpose
**As a** developer
**I need** a weather microservice with the same layered architecture as flight-status
**So that** airport weather information is available via REST API for the Python MCP server in Phase 2

##### Dependencies
- **Prerequisite Tasks**: T-006 (flight-status must be complete including tests as the reference pattern)
- **Parallel Tasks**: T-008 (gate-info can be built in parallel with weather)
- **Integration Points**: Will be called by Python MCP server in Phase 2 at port 5003
- **Blocked By**: None

#### Technical Requirements

##### Functional Requirements
- **REQ-1**: When the service starts, it shall listen on port 5003
- **REQ-2**: When `GET /api/weather` is called with an optional airport parameter, the controller shall return matching weather data
- **REQ-3**: When no weather records match the query, the controller shall return HTTP 200 with empty array `[]`
- **REQ-4**: The Swagger UI shall be accessible at `/swagger`

##### Technical Constraints
- **Technology Stack**: .NET 8, ASP.NET Core Controllers, Swashbuckle, xUnit
- **Architecture Patterns**: Identical layered structure to flight-status: CLI -> Services -> Core
- **Naming Convention**: WEATHER.CLI, WEATHER.Core, WEATHER.Services, WEATHER.Tests

#### Implementation Details

##### Files to Modify/Create
```
src/weather/
├── Dockerfile
└── src/
    ├── Weather.sln
    ├── WEATHER.CLI/
    │   ├── WEATHER.CLI.csproj
    │   ├── Program.cs                 - Swagger: "Weather API", port 5003
    │   ├── Controllers/
    │   │   └── WeatherController.cs   - GET /api/weather?airport={code}
    │   └── appsettings.json
    ├── WEATHER.Core/
    │   ├── WEATHER.Core.csproj
    │   ├── Models/
    │   │   └── AirportWeather.cs      - Weather data model (8 properties)
    │   └── Interfaces/
    │       └── IWeatherService.cs
    ├── WEATHER.Services/
    │   ├── WEATHER.Services.csproj
    │   ├── WeatherService.cs          - JSON loading + filtering
    │   └── Data/
    │       └── weather.json           - 3-5 airports, one record each
    └── WEATHER.Tests/
        ├── WEATHER.Tests.csproj
        ├── Services/
        │   └── WeatherServiceTests.cs
        └── Controllers/
            └── WeatherControllerTests.cs
```

##### Key Implementation Steps
1. **Scaffold solution and projects** (mirror T-002 with WEATHER naming) -> Solution created
2. **Create AirportWeather model** with properties: Airport, Condition, TemperatureF, TemperatureC, WindSpeed, Visibility, Humidity, LastUpdated -> Model created
3. **Create IWeatherService interface** with `GetWeather(string? airport)` -> Interface created
4. **Create WeatherService** loading weather.json with airport filtering -> Service created
5. **Create weather.json** with one weather record per airport for 3-5 airports -> Stub data created
6. **Configure Program.cs** with DI, Swagger ("Weather API"), port 5003 -> Application configured
7. **Create WeatherController** with GET /api/weather endpoint -> Controller created
8. **Create xUnit tests** for service and controller layers -> Tests created
9. **Create Dockerfile** (mirror T-007 with port 5003) -> Dockerfile created
10. **Verify**: `dotnet test`, `dotnet run`, Docker build -> All pass

##### Data Model

```csharp
// WEATHER.Core/Models/AirportWeather.cs
public class AirportWeather
{
    public string Airport { get; set; } = string.Empty;
    public string Condition { get; set; } = string.Empty;      // "Clear", "Cloudy", "Rain", "Snow", "Fog"
    public double TemperatureF { get; set; }
    public double TemperatureC { get; set; }
    public string WindSpeed { get; set; } = string.Empty;       // e.g., "15 mph NW"
    public string Visibility { get; set; } = string.Empty;      // e.g., "10 miles"
    public int Humidity { get; set; }
    public string LastUpdated { get; set; } = string.Empty;
}
```

##### API Specifications
```yaml
Method: GET
Path: /api/weather
Headers: Accept: application/json
Query Parameters:
  - airport: string (optional) - IATA airport code, case-insensitive
Response:
  - status: 200
  - body: AirportWeather[] (may be empty [])
```

#### Acceptance Criteria

##### Given-When-Then Scenarios
```gherkin
Scenario 1: Solution builds
  Given the weather solution is scaffolded
  When "dotnet build Weather.sln" is run
  Then the build succeeds with 0 errors

Scenario 2: Service starts on port 5003
  Given the application is configured
  When it is started with "dotnet run"
  Then it listens on port 5003

Scenario 3: Filter by airport
  Given the service is running with stub data
  When GET /api/weather?airport=BDL is called
  Then only BDL weather data is returned with HTTP 200

Scenario 4: No parameters returns all weather
  Given the service is running
  When GET /api/weather is called with no parameters
  Then all airport weather records are returned

Scenario 5: All tests pass
  Given all test files are created
  When "dotnet test" is run
  Then all tests pass with 0 failures

Scenario 6: Docker works
  Given the Dockerfile exists
  When the image is built and container started
  Then the service responds on port 5003
```

##### Rule-Based Criteria (Checklist)
- [ ] Solution Weather.sln builds with 0 errors
- [ ] AirportWeather model has all 8 properties from PRP specification
- [ ] TemperatureF and TemperatureC are double type; Humidity is int type
- [ ] weather.json contains one weather record per airport for 3-5 airports
- [ ] weather.json uses camelCase property names
- [ ] Service filters by airport (case-insensitive)
- [ ] Controller returns HTTP 200 for all cases (including empty results)
- [ ] Swagger UI accessible at /swagger with title "Weather API"
- [ ] Application listens on port 5003
- [ ] All xUnit tests pass
- [ ] Dockerfile builds and container runs successfully
- [ ] Project structure mirrors flight-status exactly

#### Validation & Quality Gates

##### Code Quality Checks
```bash
cd src/weather/src/
dotnet build Weather.sln
dotnet test Weather.sln --verbosity normal
# Expected: Build succeeded. All tests passed.

# Docker validation
docker build -t weather -f src/weather/Dockerfile src/weather/
docker run -d -p 5003:5003 --name w-test weather
sleep 3
curl -s http://localhost:5003/api/weather?airport=BDL
docker stop w-test && docker rm w-test
```

##### Definition of Done
- [ ] Solution builds with 0 errors
- [ ] All tests pass
- [ ] Swagger accessible on port 5003
- [ ] Docker image builds and container runs
- [ ] Structure mirrors flight-status

#### Implementation Notes
- **PATTERN**: Follow the exact same layering, naming conventions, and code patterns established by flight-status. The weather service is the simplest: only one query parameter (airport), and one record per airport in the stub data.
- **REFERENCE**: Use `src/flight-status/` as the complete reference implementation to replicate from.
- **NOTE**: The weather model includes numeric types (double for temperatures, int for humidity) unlike flight-status and gate-info which are all strings. Verify System.Text.Json handles these correctly.

---

## Implementation Recommendations

### Suggested Task Sequencing

```
Week 1 (Foundation + Pattern):
  Day 1: T-001 (.gitignore) + T-002 (scaffold)
  Day 1: T-003 (Core models)
  Day 2: T-004 (Services + stub data)
  Day 2: T-005 (CLI + Controller)
  Day 3: T-006 (xUnit tests)
  Day 3: T-007 (Dockerfile)

Week 1 (Replication - can parallelize):
  Day 4: T-008 (gate-info) -- full service
  Day 4: T-009 (weather) -- full service (parallel with T-008)
  Day 5: Final validation of all three services
```

### Suggested Team Structure

- **Single developer** can complete all tasks sequentially in 3-5 days
- **Two developers**: One takes flight-status (T-001 through T-007), second starts gate-info (T-008) once the pattern is established (after T-006), while first takes weather (T-009)
- **AI-assisted development**: With the detailed pseudocode and patterns in this document, an AI coding assistant can handle most implementation with developer review

### Parallelization Opportunities

| Parallel Group | Tasks | Condition |
|----------------|-------|-----------|
| Group 1 | T-001 + T-002 | No dependencies |
| Group 2 | T-008 + T-009 | Both depend on T-006 being complete; independent of each other |
| Group 3 | T-006 + T-007 | T-006 (tests) and T-007 (Docker) can be done in parallel after T-005 |

### Resource Allocation

- **.NET 8 SDK**: Required on development machine for all tasks
- **Docker Desktop**: Required for T-007, T-008 (Docker parts), T-009 (Docker parts)
- **IDE**: Visual Studio, Rider, or VS Code with C# extension
- **Estimated Total Effort**: 3-5 developer-days for a developer familiar with .NET

---

## Final Validation Checklist (from PRP)

After all tasks are complete, run the following comprehensive validation:

```bash
# Level 1: Build all solutions
dotnet build src/flight-status/src/FlightStatus.sln
dotnet build src/gate-info/src/GateInfo.sln
dotnet build src/weather/src/Weather.sln

# Level 2: Run all tests
dotnet test src/flight-status/src/FlightStatus.sln
dotnet test src/gate-info/src/GateInfo.sln
dotnet test src/weather/src/Weather.sln

# Level 3: Docker build and run
docker build -t flight-status -f src/flight-status/Dockerfile src/flight-status/
docker build -t gate-info -f src/gate-info/Dockerfile src/gate-info/
docker build -t weather -f src/weather/Dockerfile src/weather/

docker run -d -p 5001:5001 --name fs-test flight-status
docker run -d -p 5002:5002 --name gi-test gate-info
docker run -d -p 5003:5003 --name w-test weather
sleep 5

# Verify endpoints
curl -s http://localhost:5001/api/flights?airport=BDL
curl -s http://localhost:5002/api/gates?airport=BDL
curl -s http://localhost:5003/api/weather?airport=BDL

# Verify Swagger
curl -s http://localhost:5001/swagger/v1/swagger.json | head -1
curl -s http://localhost:5002/swagger/v1/swagger.json | head -1
curl -s http://localhost:5003/swagger/v1/swagger.json | head -1

# Verify empty results return 200
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/api/flights?airport=ZZZ
curl -s -o /dev/null -w "%{http_code}" http://localhost:5002/api/gates?airport=ZZZ
curl -s -o /dev/null -w "%{http_code}" http://localhost:5003/api/weather?airport=ZZZ

# Cleanup
docker stop fs-test gi-test w-test
docker rm fs-test gi-test w-test
```

**All commands should succeed. All HTTP status codes should be 200. All endpoints should return valid JSON.**
