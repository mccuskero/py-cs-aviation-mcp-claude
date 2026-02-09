using FLIGHTSTATUS.Services;

namespace FLIGHTSTATUS.Tests.Services;

public class FlightStatusServiceTests
{
    private readonly FlightStatusService _service;

    public FlightStatusServiceTests()
    {
        _service = new FlightStatusService();
    }

    [Fact]
    public void GetFlights_NoFilters_ReturnsAllFlights()
    {
        var results = _service.GetFlights(null, null, null);
        Assert.NotEmpty(results);
        Assert.True(results.Count() >= 15);
    }

    [Fact]
    public void GetFlights_FilterByAirport_ReturnsMatchingFlights()
    {
        var results = _service.GetFlights("BDL", null, null).ToList();
        Assert.NotEmpty(results);
        Assert.All(results, f => Assert.Equal("BDL", f.Airport));
    }

    [Fact]
    public void GetFlights_FilterByAirportCaseInsensitive_ReturnsMatchingFlights()
    {
        var results = _service.GetFlights("bdl", null, null).ToList();
        Assert.NotEmpty(results);
        Assert.All(results, f => Assert.Equal("BDL", f.Airport));
    }

    [Fact]
    public void GetFlights_FilterByFlightNumber_ReturnsMatchingFlight()
    {
        var results = _service.GetFlights(null, "DL1234", null).ToList();
        Assert.Single(results);
        Assert.Equal("DL1234", results[0].FlightNumber);
    }

    [Fact]
    public void GetFlights_FilterByTime_ReturnsMatchingFlights()
    {
        var results = _service.GetFlights(null, null, "2026-02-09").ToList();
        Assert.NotEmpty(results);
        Assert.All(results, f => Assert.StartsWith("2026-02-09", f.DepartureTime));
    }

    [Fact]
    public void GetFlights_FilterByMultipleParams_ReturnsCombinedFilter()
    {
        var results = _service.GetFlights("BDL", "DL1234", null).ToList();
        Assert.Single(results);
        Assert.Equal("BDL", results[0].Airport);
        Assert.Equal("DL1234", results[0].FlightNumber);
    }

    [Fact]
    public void GetFlights_NoMatches_ReturnsEmptyCollection()
    {
        var results = _service.GetFlights("ZZZ", null, null);
        Assert.NotNull(results);
        Assert.Empty(results);
    }
}
