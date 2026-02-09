using System.Net;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc.Testing;
using FLIGHTSTATUS.Core.Models;

namespace FLIGHTSTATUS.Tests.Controllers;

public class FlightsControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    private readonly JsonSerializerOptions _jsonOptions = new() { PropertyNameCaseInsensitive = true };

    public FlightsControllerTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task Get_NoParams_Returns200WithFlights()
    {
        var response = await _client.GetAsync("/api/flights");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        var flights = JsonSerializer.Deserialize<List<Flight>>(content, _jsonOptions);
        Assert.NotNull(flights);
        Assert.NotEmpty(flights);
    }

    [Fact]
    public async Task Get_WithAirport_Returns200WithFilteredFlights()
    {
        var response = await _client.GetAsync("/api/flights?airport=BDL");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        var flights = JsonSerializer.Deserialize<List<Flight>>(content, _jsonOptions);
        Assert.NotNull(flights);
        Assert.NotEmpty(flights);
        Assert.All(flights, f => Assert.Equal("BDL", f.Airport));
    }

    [Fact]
    public async Task Get_NoMatches_Returns200WithEmptyArray()
    {
        var response = await _client.GetAsync("/api/flights?airport=ZZZ");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        var flights = JsonSerializer.Deserialize<List<Flight>>(content, _jsonOptions);
        Assert.NotNull(flights);
        Assert.Empty(flights);
    }

    [Fact]
    public async Task Get_SwaggerEndpoint_Returns200()
    {
        var response = await _client.GetAsync("/swagger/v1/swagger.json");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
