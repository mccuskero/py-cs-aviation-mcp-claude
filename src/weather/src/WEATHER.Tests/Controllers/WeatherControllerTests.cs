using System.Net;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc.Testing;
using WEATHER.Core.Models;

namespace WEATHER.Tests.Controllers;

public class WeatherControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    private readonly JsonSerializerOptions _jsonOptions = new() { PropertyNameCaseInsensitive = true };

    public WeatherControllerTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task Get_NoParams_Returns200WithAllWeather()
    {
        var response = await _client.GetAsync("/api/weather");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        var weather = JsonSerializer.Deserialize<List<AirportWeather>>(content, _jsonOptions);
        Assert.NotNull(weather);
        Assert.Equal(5, weather.Count);
    }

    [Fact]
    public async Task Get_WithAirport_Returns200WithFilteredWeather()
    {
        var response = await _client.GetAsync("/api/weather?airport=BDL");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        var weather = JsonSerializer.Deserialize<List<AirportWeather>>(content, _jsonOptions);
        Assert.NotNull(weather);
        Assert.Single(weather);
        Assert.Equal("BDL", weather[0].Airport);
    }

    [Fact]
    public async Task Get_NoMatches_Returns200WithEmptyArray()
    {
        var response = await _client.GetAsync("/api/weather?airport=ZZZ");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        var weather = JsonSerializer.Deserialize<List<AirportWeather>>(content, _jsonOptions);
        Assert.NotNull(weather);
        Assert.Empty(weather);
    }

    [Fact]
    public async Task Get_SwaggerEndpoint_Returns200()
    {
        var response = await _client.GetAsync("/swagger/v1/swagger.json");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
