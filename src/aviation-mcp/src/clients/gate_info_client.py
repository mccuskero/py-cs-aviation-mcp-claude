from src.clients.base import BaseServiceClient
from src.models.gate import Gate


class GateInfoClient(BaseServiceClient):
    """HTTP client for the gate-info C# microservice."""

    def __init__(self, base_url: str):
        super().__init__(base_url)

    async def get_gates(
        self, airport: str = "", gate_number: str = ""
    ) -> list[Gate]:
        data = await self.get(
            "/api/gates",
            {"airport": airport, "gateNumber": gate_number},
        )
        return [Gate(**item) for item in data]
