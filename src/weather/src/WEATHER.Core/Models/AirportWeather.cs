namespace WEATHER.Core.Models;

public class AirportWeather
{
    public string Airport { get; set; } = string.Empty;
    public string Condition { get; set; } = string.Empty;
    public double TemperatureF { get; set; }
    public double TemperatureC { get; set; }
    public string WindSpeed { get; set; } = string.Empty;
    public string Visibility { get; set; } = string.Empty;
    public int Humidity { get; set; }
    public string LastUpdated { get; set; } = string.Empty;
}
