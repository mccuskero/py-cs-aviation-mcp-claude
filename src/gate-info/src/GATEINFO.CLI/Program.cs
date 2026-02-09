using GATEINFO.Core.Interfaces;
using GATEINFO.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new() { Title = "Gate Info API", Version = "v1" });
});

builder.Services.AddSingleton<IGateInfoService, GateInfoService>();

builder.WebHost.UseUrls("http://0.0.0.0:5002");

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();
app.MapControllers();
app.Run();

public partial class Program { }
