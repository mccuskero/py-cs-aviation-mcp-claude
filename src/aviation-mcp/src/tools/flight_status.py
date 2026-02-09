import logging

import httpx

from src.clients.flight_status_client import FlightStatusClient
from src.config import Config
from src.tools.base import BaseTool

logger = logging.getLogger(__name__)


class FlightStatusTool(BaseTool):
    """Handler for the get_flight_status MCP tool."""

    def __init__(self, config: Config):
        super().__init__(config)
        self.client = FlightStatusClient(config.flight_status_url)

    async def execute(
        self, airport: str = "", flight_number: str = "", time: str = ""
    ) -> str:
        try:
            flights = await self.client.get_flights(
                airport=airport, flight_number=flight_number, time=time
            )
            if not flights:
                return "No flights found matching the criteria."
            results = []
            for f in flights:
                results.append(
                    f"Flight {f.flight_number} ({f.airline}): "
                    f"{f.origin} -> {f.destination}, "
                    f"Status: {f.status}, Gate: {f.gate}"
                )
            return "\n".join(results)
        except httpx.ConnectError:
            return "Error: Flight status service is unavailable."
        except httpx.TimeoutException:
            return "Error: Flight status service timed out."
        except httpx.HTTPStatusError as e:
            return f"Error: Flight status service returned {e.response.status_code}."
