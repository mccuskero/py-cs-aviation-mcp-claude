using WEATHER.Core.Models;

namespace WEATHER.Core.Interfaces;

public interface IWeatherService
{
    IEnumerable<AirportWeather> GetWeather(string? airport);
}
