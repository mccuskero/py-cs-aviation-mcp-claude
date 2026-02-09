FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src
COPY src/ .
RUN dotnet restore GateInfo.sln
RUN dotnet publish GATEINFO.CLI/GATEINFO.CLI.csproj -c Release -o /app

FROM mcr.microsoft.com/dotnet/aspnet:9.0
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=build /app .
ENV ASPNETCORE_HTTP_PORTS=5002
EXPOSE 5002
ENTRYPOINT ["dotnet", "GATEINFO.CLI.dll"]
