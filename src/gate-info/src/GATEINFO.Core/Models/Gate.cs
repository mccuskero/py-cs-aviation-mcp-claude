namespace GATEINFO.Core.Models;

public class Gate
{
    public string Airport { get; set; } = string.Empty;
    public string GateNumber { get; set; } = string.Empty;
    public string Terminal { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public string AssignedFlight { get; set; } = string.Empty;
    public string Airline { get; set; } = string.Empty;
    public string LastUpdated { get; set; } = string.Empty;
}
