from unittest.mock import AsyncMock, patch

import httpx
import pytest

from src.models.weather import AirportWeather
from src.tools.weather import WeatherTool


@pytest.mark.asyncio
async def test_execute_returns_formatted_string(config):
    tool = WeatherTool(config)
    mock_weather = [
        AirportWeather(
            airport="BDL",
            condition="Clear",
            temperature_f=28.0,
            temperature_c=-2.2,
            wind_speed="10 mph NW",
            visibility="10 miles",
            humidity=45,
            last_updated="2026-02-09T12:00:00Z",
        )
    ]
    with patch.object(
        tool.client, "get_weather", new_callable=AsyncMock, return_value=mock_weather
    ):
        result = await tool.execute(airport="BDL")
    assert "BDL" in result
    assert "Clear" in result
    assert "28.0" in result
    assert "45%" in result


@pytest.mark.asyncio
async def test_execute_no_results(config):
    tool = WeatherTool(config)
    with patch.object(tool.client, "get_weather", new_callable=AsyncMock, return_value=[]):
        result = await tool.execute(airport="ZZZ")
    assert "No weather data found" in result


@pytest.mark.asyncio
async def test_execute_service_unavailable(config):
    tool = WeatherTool(config)
    with patch.object(
        tool.client, "get_weather", new_callable=AsyncMock, side_effect=httpx.ConnectError("")
    ):
        result = await tool.execute(airport="BDL")
    assert "Error" in result
    assert "unavailable" in result
