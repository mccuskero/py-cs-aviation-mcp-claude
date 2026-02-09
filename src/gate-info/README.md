# Gate Info Service

C# ASP.NET Core microservice providing airport gate information from parameterized JSON stub data.

## API

```
GET /api/gates?airport={code}&gateNumber={number}
```

All parameters are optional query parameters. Omitting a parameter skips that filter.

| Parameter | Example | Description |
|-----------|---------|-------------|
| `airport` | JFK | IATA airport code |
| `gateNumber` | C22 | Gate identifier |

### Response

Returns `200 OK` with a JSON array of gates. Returns an empty array `[]` for no matches.

```json
[
  {
    "airport": "JFK",
    "gateNumber": "C22",
    "terminal": "C",
    "status": "Boarding",
    "assignedFlight": "DL400",
    "airline": "Delta",
    "lastUpdated": "2026-02-09T08:45:00Z"
  }
]
```

### Swagger

Available at `/swagger` when the service is running.

## Stub Data

The service loads gate records from `GATEINFO.Services/Data/gates.json`. Five airports with 3-4 gates each:

| Airport | Gates | Statuses |
|---------|-------|----------|
| BDL | A1, A8, B1, B3 | Boarding, Open, Closed |
| JFK | C22, D7, B14 | Boarding, Open |
| LAX | 71A, 52B, 40C | Closed, Open, Maintenance |
| ORD | C18, H12, A5 | Open, Boarding |
| ATL | T4, A22, C10, B8 | Open, Boarding, Closed, Maintenance |

## Project Structure

```
src/gate-info/
├── Dockerfile
└── src/
    ├── GateInfo.sln
    ├── GATEINFO.CLI/               # ASP.NET Core entry point
    │   ├── Program.cs
    │   └── Controllers/
    │       └── GatesController.cs
    ├── GATEINFO.Core/              # Models and interfaces
    │   ├── Models/
    │   │   └── Gate.cs
    │   └── Interfaces/
    │       └── IGateInfoService.cs
    ├── GATEINFO.Services/          # Business logic
    │   ├── GateInfoService.cs
    │   └── Data/
    │       └── gates.json
    └── GATEINFO.Tests/             # xUnit tests
        ├── Services/
        └── Controllers/
```

## Running

### Local

```bash
cd src && dotnet run --project GATEINFO.CLI
```

Starts on `http://localhost:5002`.

### Docker

```bash
docker build -t gate-info .
docker run -p 5002:5002 gate-info
```

### Via Docker Compose (from project root)

```bash
docker-compose up --build gate-info
```

## Testing

```bash
cd src && dotnet test --verbosity normal
```

10 xUnit tests covering:
- **Service layer**: Filtering by airport, gate number; empty results for unknown params
- **Controller layer**: HTTP 200 responses, JSON serialization, query parameter binding

## Design

Follows the **Controller -> Service -> Core** layering pattern:

- **Controller** handles HTTP concerns (query params, response codes)
- **Service** loads JSON data and applies parameterized filters
- **Core** defines the `Gate` model and `IGateInfoService` interface
- **Service registered as Singleton** via DI — JSON data loaded once at startup
