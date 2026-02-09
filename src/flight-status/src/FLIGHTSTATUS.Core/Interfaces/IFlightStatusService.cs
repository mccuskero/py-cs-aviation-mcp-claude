using FLIGHTSTATUS.Core.Models;

namespace FLIGHTSTATUS.Core.Interfaces;

public interface IFlightStatusService
{
    IEnumerable<Flight> GetFlights(string? airport, string? flightNumber, string? time);
}
