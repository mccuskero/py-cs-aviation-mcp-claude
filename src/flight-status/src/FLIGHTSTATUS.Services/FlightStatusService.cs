using System.Reflection;
using System.Text.Json;
using FLIGHTSTATUS.Core.Interfaces;
using FLIGHTSTATUS.Core.Models;

namespace FLIGHTSTATUS.Services;

public class FlightStatusService : IFlightStatusService
{
    private readonly List<Flight> _flights;

    public FlightStatusService()
    {
        var assemblyDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location)!;
        var json = File.ReadAllText(Path.Combine(assemblyDir, "Data", "flights.json"));
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
