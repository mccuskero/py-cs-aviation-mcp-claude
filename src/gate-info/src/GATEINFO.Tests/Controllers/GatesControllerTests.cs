using System.Net;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc.Testing;
using GATEINFO.Core.Models;

namespace GATEINFO.Tests.Controllers;

public class GatesControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    private readonly JsonSerializerOptions _jsonOptions = new() { PropertyNameCaseInsensitive = true };

    public GatesControllerTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task Get_NoParams_Returns200WithGates()
    {
        var response = await _client.GetAsync("/api/gates");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        var gates = JsonSerializer.Deserialize<List<Gate>>(content, _jsonOptions);
        Assert.NotNull(gates);
        Assert.NotEmpty(gates);
    }

    [Fact]
    public async Task Get_WithAirport_Returns200WithFilteredGates()
    {
        var response = await _client.GetAsync("/api/gates?airport=BDL");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        var gates = JsonSerializer.Deserialize<List<Gate>>(content, _jsonOptions);
        Assert.NotNull(gates);
        Assert.NotEmpty(gates);
        Assert.All(gates, g => Assert.Equal("BDL", g.Airport));
    }

    [Fact]
    public async Task Get_NoMatches_Returns200WithEmptyArray()
    {
        var response = await _client.GetAsync("/api/gates?airport=ZZZ");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        var gates = JsonSerializer.Deserialize<List<Gate>>(content, _jsonOptions);
        Assert.NotNull(gates);
        Assert.Empty(gates);
    }

    [Fact]
    public async Task Get_SwaggerEndpoint_Returns200()
    {
        var response = await _client.GetAsync("/swagger/v1/swagger.json");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
