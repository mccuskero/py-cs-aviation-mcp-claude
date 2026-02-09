import logging

import httpx

from src.clients.gate_info_client import GateInfoClient
from src.config import Config
from src.tools.base import BaseTool

logger = logging.getLogger(__name__)


class GateInfoTool(BaseTool):
    """Handler for the get_gate_info MCP tool."""

    def __init__(self, config: Config):
        super().__init__(config)
        self.client = GateInfoClient(config.gate_info_url)

    async def execute(self, airport: str = "", gate_number: str = "") -> str:
        try:
            gates = await self.client.get_gates(airport=airport, gate_number=gate_number)
            if not gates:
                return "No gate information found matching the criteria."
            results = []
            for g in gates:
                results.append(
                    f"Gate {g.gate_number} ({g.terminal}): "
                    f"Status: {g.status}, "
                    f"Flight: {g.assigned_flight}, Airline: {g.airline}"
                )
            return "\n".join(results)
        except httpx.ConnectError:
            return "Error: Gate info service is unavailable."
        except httpx.TimeoutException:
            return "Error: Gate info service timed out."
        except httpx.HTTPStatusError as e:
            return f"Error: Gate info service returned {e.response.status_code}."
