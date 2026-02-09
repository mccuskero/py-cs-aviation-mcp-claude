import pytest

from src.clients.weather_client import WeatherClient


@pytest.mark.asyncio
async def test_get_weather_success(httpx_mock, sample_weather_data):
    httpx_mock.add_response(json=sample_weather_data)
    client = WeatherClient("http://localhost:5003")
    weather = await client.get_weather(airport="BDL")
    assert len(weather) == 1
    assert weather[0].airport == "BDL"
    assert weather[0].temperature_f == 28.0
    assert weather[0].humidity == 45


@pytest.mark.asyncio
async def test_get_weather_empty(httpx_mock):
    httpx_mock.add_response(json=[])
    client = WeatherClient("http://localhost:5003")
    weather = await client.get_weather(airport="ZZZ")
    assert weather == []
