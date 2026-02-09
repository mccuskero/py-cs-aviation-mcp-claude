using WEATHER.Core.Interfaces;
using WEATHER.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new() { Title = "Weather API", Version = "v1" });
});

builder.Services.AddSingleton<IWeatherService, WeatherService>();

builder.WebHost.UseUrls("http://0.0.0.0:5003");

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();
app.MapControllers();
app.Run();

public partial class Program { }
