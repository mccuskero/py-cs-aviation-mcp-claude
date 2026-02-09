using GATEINFO.Services;

namespace GATEINFO.Tests.Services;

public class GateInfoServiceTests
{
    private readonly GateInfoService _service;

    public GateInfoServiceTests()
    {
        _service = new GateInfoService();
    }

    [Fact]
    public void GetGates_NoFilters_ReturnsAllGates()
    {
        var results = _service.GetGates(null, null);
        Assert.NotEmpty(results);
        Assert.True(results.Count() >= 15);
    }

    [Fact]
    public void GetGates_FilterByAirport_ReturnsMatchingGates()
    {
        var results = _service.GetGates("BDL", null).ToList();
        Assert.NotEmpty(results);
        Assert.All(results, g => Assert.Equal("BDL", g.Airport));
    }

    [Fact]
    public void GetGates_FilterByAirportCaseInsensitive_ReturnsMatchingGates()
    {
        var results = _service.GetGates("bdl", null).ToList();
        Assert.NotEmpty(results);
        Assert.All(results, g => Assert.Equal("BDL", g.Airport));
    }

    [Fact]
    public void GetGates_FilterByGateNumber_ReturnsMatchingGate()
    {
        var results = _service.GetGates(null, "A1").ToList();
        Assert.Single(results);
        Assert.Equal("A1", results[0].GateNumber);
    }

    [Fact]
    public void GetGates_FilterByMultipleParams_ReturnsCombinedFilter()
    {
        var results = _service.GetGates("BDL", "A1").ToList();
        Assert.Single(results);
        Assert.Equal("BDL", results[0].Airport);
        Assert.Equal("A1", results[0].GateNumber);
    }

    [Fact]
    public void GetGates_NoMatches_ReturnsEmptyCollection()
    {
        var results = _service.GetGates("ZZZ", null);
        Assert.NotNull(results);
        Assert.Empty(results);
    }
}
