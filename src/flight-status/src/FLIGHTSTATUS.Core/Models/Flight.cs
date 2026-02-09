namespace FLIGHTSTATUS.Core.Models;

public class Flight
{
    public string Airport { get; set; } = string.Empty;
    public string FlightNumber { get; set; } = string.Empty;
    public string Airline { get; set; } = string.Empty;
    public string Origin { get; set; } = string.Empty;
    public string Destination { get; set; } = string.Empty;
    public string DepartureTime { get; set; } = string.Empty;
    public string ArrivalTime { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public string Gate { get; set; } = string.Empty;
    public string Terminal { get; set; } = string.Empty;
}
