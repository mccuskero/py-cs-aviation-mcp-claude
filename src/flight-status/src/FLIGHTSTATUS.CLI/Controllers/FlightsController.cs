using Microsoft.AspNetCore.Mvc;
using FLIGHTSTATUS.Core.Interfaces;
using FLIGHTSTATUS.Core.Models;

namespace FLIGHTSTATUS.CLI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class FlightsController : ControllerBase
{
    private readonly IFlightStatusService _service;

    public FlightsController(IFlightStatusService service) => _service = service;

    [HttpGet]
    public ActionResult<IEnumerable<Flight>> Get(
        [FromQuery] string? airport,
        [FromQuery] string? flightNumber,
        [FromQuery] string? time)
    {
        var results = _service.GetFlights(airport, flightNumber, time);
        return Ok(results);
    }
}
