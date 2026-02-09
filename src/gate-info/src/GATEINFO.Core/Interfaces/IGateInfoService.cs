using GATEINFO.Core.Models;

namespace GATEINFO.Core.Interfaces;

public interface IGateInfoService
{
    IEnumerable<Gate> GetGates(string? airport, string? gateNumber);
}
