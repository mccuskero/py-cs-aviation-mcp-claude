FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src
COPY src/ .
RUN dotnet restore Weather.sln
RUN dotnet publish WEATHER.CLI/WEATHER.CLI.csproj -c Release -o /app

FROM mcr.microsoft.com/dotnet/aspnet:9.0
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=build /app .
ENV ASPNETCORE_HTTP_PORTS=5003
EXPOSE 5003
ENTRYPOINT ["dotnet", "WEATHER.CLI.dll"]
