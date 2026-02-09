aviavation-mcp is a Model Context Protocol (MCP) server for airport and flight information connect AI agents to real-time aviation data, such as flight statuses, gate information, delays, and scheduling.

This mcp server will call on three c# based microservices, whcih are stubbed out with static information loaded from a json file.

There will be 3 different test services

1. flight-status parameters: airport name e.g., BDL, flight_number 1234, time
2. gate-info - airport name, gate_number
3. weather - airport name

The test services will be:

- programmed in C#
- will use swagger 

The mcp server will be written using python 3.13, and will use

- langchain v1.2.6+.
- use uv package manager to manage python packages
- use Object orientted style of programming

The mcp server will be call on these services for flight-status, gate-info, and weather.

We will create a separate CLI based mcp client to test the MCP server.

The project structure will look like

py-cs-aviation-mcp-claude
    docker-compose.yml
    src
        aviation-mcp
            Dockerfile
            src
        flight-status
            Dockerfile
            src
                FLIGHTSTATUS.CLI
                FLIGHTSTATUS.Core
                FLIGHTSTATUS.Services
                FLIGHTSTATUS.Tests
        gate-info
            Dockerfile
            src
                GATEINFO.CLI
                GATEINFO.Core
                GATEINFO.Services
                GATEINFO.Tests
        weather
            Dockerfile
            src
                WEATHER.CLI
                WEATHER.Core
                WEATHER.Services
                WEATHER.Tests

We will use a Dockerfile for each application
We will use a docker-compose to stand up the services.

The project will have multiple phases:

- create stubbed mircoservices
- create mcp server 
- create test client using mcp client