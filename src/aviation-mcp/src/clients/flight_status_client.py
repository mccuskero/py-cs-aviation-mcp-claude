from src.clients.base import BaseServiceClient
from src.models.flight import Flight


class FlightStatusClient(BaseServiceClient):
    """HTTP client for the flight-status C# microservice."""

    def __init__(self, base_url: str):
        super().__init__(base_url)

    async def get_flights(
        self, airport: str = "", flight_number: str = "", time: str = ""
    ) -> list[Flight]:
        data = await self.get(
            "/api/flights",
            {"airport": airport, "flightNumber": flight_number, "time": time},
        )
        return [Flight(**item) for item in data]
