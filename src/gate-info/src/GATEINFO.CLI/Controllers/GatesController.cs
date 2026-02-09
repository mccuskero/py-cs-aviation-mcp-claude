using Microsoft.AspNetCore.Mvc;
using GATEINFO.Core.Interfaces;
using GATEINFO.Core.Models;

namespace GATEINFO.CLI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class GatesController : ControllerBase
{
    private readonly IGateInfoService _service;

    public GatesController(IGateInfoService service) => _service = service;

    [HttpGet]
    public ActionResult<IEnumerable<Gate>> Get(
        [FromQuery] string? airport,
        [FromQuery] string? gateNumber)
    {
        var results = _service.GetGates(airport, gateNumber);
        return Ok(results);
    }
}
