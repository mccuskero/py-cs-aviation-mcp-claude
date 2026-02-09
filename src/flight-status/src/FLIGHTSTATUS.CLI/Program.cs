using FLIGHTSTATUS.Core.Interfaces;
using FLIGHTSTATUS.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new() { Title = "Flight Status API", Version = "v1" });
});

builder.Services.AddSingleton<IFlightStatusService, FlightStatusService>();

builder.WebHost.UseUrls("http://0.0.0.0:5001");

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();
app.MapControllers();
app.Run();

public partial class Program { }
