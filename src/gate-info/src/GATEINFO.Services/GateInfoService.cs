using System.Reflection;
using System.Text.Json;
using GATEINFO.Core.Interfaces;
using GATEINFO.Core.Models;

namespace GATEINFO.Services;

public class GateInfoService : IGateInfoService
{
    private readonly List<Gate> _gates;

    public GateInfoService()
    {
        var assemblyDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location)!;
        var json = File.ReadAllText(Path.Combine(assemblyDir, "Data", "gates.json"));
        _gates = JsonSerializer.Deserialize<List<Gate>>(json,
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true }) ?? new();
    }

    public IEnumerable<Gate> GetGates(string? airport, string? gateNumber)
    {
        var query = _gates.AsEnumerable();
        if (!string.IsNullOrEmpty(airport))
            query = query.Where(g => g.Airport.Equals(airport, StringComparison.OrdinalIgnoreCase));
        if (!string.IsNullOrEmpty(gateNumber))
            query = query.Where(g => g.GateNumber == gateNumber);
        return query.ToList();
    }
}
