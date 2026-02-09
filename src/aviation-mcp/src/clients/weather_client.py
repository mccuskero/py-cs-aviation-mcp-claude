from src.clients.base import BaseServiceClient
from src.models.weather import AirportWeather


class WeatherClient(BaseServiceClient):
    """HTTP client for the weather C# microservice."""

    def __init__(self, base_url: str):
        super().__init__(base_url)

    async def get_weather(self, airport: str = "") -> list[AirportWeather]:
        data = await self.get("/api/weather", {"airport": airport})
        return [AirportWeather(**item) for item in data]
