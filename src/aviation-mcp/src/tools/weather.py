import logging

import httpx

from src.clients.weather_client import WeatherClient
from src.config import Config
from src.tools.base import BaseTool

logger = logging.getLogger(__name__)


class WeatherTool(BaseTool):
    """Handler for the get_weather MCP tool."""

    def __init__(self, config: Config):
        super().__init__(config)
        self.client = WeatherClient(config.weather_url)

    async def execute(self, airport: str = "") -> str:
        try:
            weather = await self.client.get_weather(airport=airport)
            if not weather:
                return "No weather data found for the specified airport."
            results = []
            for w in weather:
                results.append(
                    f"{w.airport}: {w.condition}, "
                    f"{w.temperature_f}°F / {w.temperature_c}°C, "
                    f"Wind: {w.wind_speed}, Visibility: {w.visibility}, "
                    f"Humidity: {w.humidity}%"
                )
            return "\n".join(results)
        except httpx.ConnectError:
            return "Error: Weather service is unavailable."
        except httpx.TimeoutException:
            return "Error: Weather service timed out."
        except httpx.HTTPStatusError as e:
            return f"Error: Weather service returned {e.response.status_code}."
