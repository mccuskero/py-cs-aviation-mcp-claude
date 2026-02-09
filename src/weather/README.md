# Weather Service

C# ASP.NET Core microservice providing airport weather conditions from parameterized JSON stub data.

## API

```
GET /api/weather?airport={code}
```

The airport parameter is optional. Omitting it returns weather for all airports.

| Parameter | Example | Description |
|-----------|---------|-------------|
| `airport` | LAX | IATA airport code |

### Response

Returns `200 OK` with a JSON array of weather records. Returns an empty array `[]` for no matches.

```json
[
  {
    "airport": "LAX",
    "condition": "Clear",
    "temperatureF": 68.0,
    "temperatureC": 20.0,
    "windSpeed": "5 mph W",
    "visibility": "10 miles",
    "humidity": 40,
    "lastUpdated": "2026-02-09T06:00:00Z"
  }
]
```

### Swagger

Available at `/swagger` when the service is running.

## Stub Data

The service loads weather records from `WEATHER.Services/Data/weather.json`. One record per airport:

| Airport | Condition | Temp (F) | Wind | Humidity |
|---------|-----------|----------|------|----------|
| BDL | Clear | 28 | 10 mph NW | 45% |
| JFK | Cloudy | 35 | 15 mph NE | 62% |
| LAX | Clear | 68 | 5 mph W | 40% |
| ORD | Snow | 22 | 20 mph N | 78% |
| ATL | Rain | 48 | 12 mph SE | 85% |

## Project Structure

```
src/weather/
├── Dockerfile
└── src/
    ├── Weather.sln
    ├── WEATHER.CLI/                # ASP.NET Core entry point
    │   ├── Program.cs
    │   └── Controllers/
    │       └── WeatherController.cs
    ├── WEATHER.Core/               # Models and interfaces
    │   ├── Models/
    │   │   └── AirportWeather.cs
    │   └── Interfaces/
    │       └── IWeatherService.cs
    ├── WEATHER.Services/           # Business logic
    │   ├── WeatherService.cs
    │   └── Data/
    │       └── weather.json
    └── WEATHER.Tests/              # xUnit tests
        ├── Services/
        └── Controllers/
```

## Running

### Local

```bash
cd src && dotnet run --project WEATHER.CLI
```

Starts on `http://localhost:5003`.

### Docker

```bash
docker build -t weather .
docker run -p 5003:5003 weather
```

### Via Docker Compose (from project root)

```bash
docker-compose up --build weather
```

## Testing

```bash
cd src && dotnet test --verbosity normal
```

9 xUnit tests covering:
- **Service layer**: Filtering by airport; empty results for unknown airports
- **Controller layer**: HTTP 200 responses, JSON serialization, query parameter binding

## Design

Follows the **Controller -> Service -> Core** layering pattern:

- **Controller** handles HTTP concerns (query params, response codes)
- **Service** loads JSON data and applies parameterized filters
- **Core** defines the `AirportWeather` model and `IWeatherService` interface
- **Service registered as Singleton** via DI — JSON data loaded once at startup
