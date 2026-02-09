using WEATHER.Services;

namespace WEATHER.Tests.Services;

public class WeatherServiceTests
{
    private readonly WeatherService _service;

    public WeatherServiceTests()
    {
        _service = new WeatherService();
    }

    [Fact]
    public void GetWeather_NoFilter_ReturnsAllRecords()
    {
        var results = _service.GetWeather(null);
        Assert.NotEmpty(results);
        Assert.Equal(5, results.Count());
    }

    [Fact]
    public void GetWeather_FilterByAirport_ReturnsMatchingRecord()
    {
        var results = _service.GetWeather("BDL").ToList();
        Assert.Single(results);
        Assert.Equal("BDL", results[0].Airport);
    }

    [Fact]
    public void GetWeather_FilterByAirportCaseInsensitive_ReturnsMatchingRecord()
    {
        var results = _service.GetWeather("bdl").ToList();
        Assert.Single(results);
        Assert.Equal("BDL", results[0].Airport);
    }

    [Fact]
    public void GetWeather_NumericFieldsDeserialize_CorrectTypes()
    {
        var results = _service.GetWeather("BDL").ToList();
        Assert.Single(results);
        Assert.Equal(28.0, results[0].TemperatureF);
        Assert.Equal(-2.2, results[0].TemperatureC);
        Assert.Equal(45, results[0].Humidity);
    }

    [Fact]
    public void GetWeather_NoMatches_ReturnsEmptyCollection()
    {
        var results = _service.GetWeather("ZZZ");
        Assert.NotNull(results);
        Assert.Empty(results);
    }
}
