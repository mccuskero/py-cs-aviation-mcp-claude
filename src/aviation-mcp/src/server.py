import argparse

from mcp.server.fastmcp import FastMCP

from src.config import Config
from src.debug_logging.protocol_logger import setup_protocol_logging
from src.tools.flight_status import FlightStatusTool
from src.tools.gate_info import GateInfoTool
from src.tools.weather import WeatherTool

mcp_server = FastMCP("aviation-mcp", host="0.0.0.0", port=8000)
config = Config()


@mcp_server.tool()
async def get_flight_status(
    airport: str = "", flight_number: str = "", time: str = ""
) -> str:
    """Get flight status information for an airport.

    Args:
        airport: IATA airport code (e.g., BDL, JFK)
        flight_number: Flight number (e.g., DL1234)
        time: Departure time filter (ISO 8601 prefix)
    """
    tool = FlightStatusTool(config)
    return await tool.execute(airport=airport, flight_number=flight_number, time=time)


@mcp_server.tool()
async def get_gate_info(airport: str = "", gate_number: str = "") -> str:
    """Get gate information for an airport.

    Args:
        airport: IATA airport code (e.g., BDL, JFK)
        gate_number: Gate identifier (e.g., A1, B12)
    """
    tool = GateInfoTool(config)
    return await tool.execute(airport=airport, gate_number=gate_number)


@mcp_server.tool()
async def get_weather(airport: str = "") -> str:
    """Get current weather conditions for an airport.

    Args:
        airport: IATA airport code (e.g., BDL, JFK)
    """
    tool = WeatherTool(config)
    return await tool.execute(airport=airport)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aviation MCP Server")
    parser.add_argument("--debug", action="store_true", help="Enable protocol debug logging")
    args = parser.parse_args()

    if args.debug or config.debug:
        setup_protocol_logging()

    mcp_server.run(transport="sse")
