# Flight Status Service

C# ASP.NET Core microservice providing flight status information from parameterized JSON stub data.

## API

```
GET /api/flights?airport={code}&flightNumber={number}&time={time}
```

All parameters are optional query parameters. Omitting a parameter skips that filter.

| Parameter | Example | Description |
|-----------|---------|-------------|
| `airport` | BDL | IATA airport code |
| `flightNumber` | DL1234 | Flight number |
| `time` | 2026-02-09T14:30 | Departure time prefix (ISO 8601) |

### Response

Returns `200 OK` with a JSON array of flights. Returns an empty array `[]` for no matches.

```json
[
  {
    "airport": "BDL",
    "flightNumber": "DL1234",
    "airline": "Delta",
    "origin": "BDL",
    "destination": "ATL",
    "departureTime": "2026-02-09T14:30:00Z",
    "arrivalTime": "2026-02-09T17:30:00Z",
    "status": "On Time",
    "gate": "A12",
    "terminal": "A"
  }
]
```

### Swagger

Available at `/swagger` when the service is running.

## Stub Data

The service loads flight records from `FLIGHTSTATUS.Services/Data/flights.json`. Five airports with 3-4 flights each:

| Airport | Flights | Statuses |
|---------|---------|----------|
| BDL | DL1234, UA567, AA890, SW321 | On Time, Delayed |
| JFK | DL400, BA178, AA100 | On Time, Boarding |
| LAX | UA200, DL555, AA750 | Departed, On Time |
| ORD | UA300, AA450, SW800 | On Time, Delayed |
| ATL | DL900, DL950, SW150, UA675 | On Time, Cancelled |

## Project Structure

```
src/flight-status/
├── Dockerfile
└── src/
    ├── FlightStatus.sln
    ├── FLIGHTSTATUS.CLI/           # ASP.NET Core entry point
    │   ├── Program.cs              # Host builder, Swagger, DI
    │   └── Controllers/
    │       └── FlightsController.cs
    ├── FLIGHTSTATUS.Core/          # Models and interfaces
    │   ├── Models/
    │   │   └── Flight.cs
    │   └── Interfaces/
    │       └── IFlightStatusService.cs
    ├── FLIGHTSTATUS.Services/      # Business logic
    │   ├── FlightStatusService.cs  # JSON loading, parameterized filtering
    │   └── Data/
    │       └── flights.json        # Stub data
    └── FLIGHTSTATUS.Tests/         # xUnit tests
        ├── Services/               # Service layer tests
        └── Controllers/            # Controller layer tests
```

## Running

### Local

```bash
cd src && dotnet run --project FLIGHTSTATUS.CLI
```

Starts on `http://localhost:5001`.

### Docker

```bash
docker build -t flight-status .
docker run -p 5001:5001 flight-status
```

### Via Docker Compose (from project root)

```bash
docker-compose up --build flight-status
```

## Testing

```bash
cd src && dotnet test --verbosity normal
```

11 xUnit tests covering:
- **Service layer**: Filtering by airport, flight number, time; empty results for unknown params
- **Controller layer**: HTTP 200 responses, JSON serialization, query parameter binding

## Design

Follows the **Controller -> Service -> Core** layering pattern:

- **Controller** handles HTTP concerns (query params, response codes)
- **Service** loads JSON data and applies parameterized filters
- **Core** defines the `Flight` model and `IFlightStatusService` interface
- **Service registered as Singleton** via DI — JSON data loaded once at startup
