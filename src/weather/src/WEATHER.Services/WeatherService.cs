using System.Reflection;
using System.Text.Json;
using WEATHER.Core.Interfaces;
using WEATHER.Core.Models;

namespace WEATHER.Services;

public class WeatherService : IWeatherService
{
    private readonly List<AirportWeather> _weather;

    public WeatherService()
    {
        var assemblyDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location)!;
        var json = File.ReadAllText(Path.Combine(assemblyDir, "Data", "weather.json"));
        _weather = JsonSerializer.Deserialize<List<AirportWeather>>(json,
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true }) ?? new();
    }

    public IEnumerable<AirportWeather> GetWeather(string? airport)
    {
        var query = _weather.AsEnumerable();
        if (!string.IsNullOrEmpty(airport))
            query = query.Where(w => w.Airport.Equals(airport, StringComparison.OrdinalIgnoreCase));
        return query.ToList();
    }
}
