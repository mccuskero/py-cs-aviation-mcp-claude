using Microsoft.AspNetCore.Mvc;
using WEATHER.Core.Interfaces;
using WEATHER.Core.Models;

namespace WEATHER.CLI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class WeatherController : ControllerBase
{
    private readonly IWeatherService _service;

    public WeatherController(IWeatherService service) => _service = service;

    [HttpGet]
    public ActionResult<IEnumerable<AirportWeather>> Get(
        [FromQuery] string? airport)
    {
        var results = _service.GetWeather(airport);
        return Ok(results);
    }
}
