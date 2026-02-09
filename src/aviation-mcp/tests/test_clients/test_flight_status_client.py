import pytest

from src.clients.flight_status_client import FlightStatusClient


@pytest.mark.asyncio
async def test_get_flights_success(httpx_mock, sample_flight_data):
    httpx_mock.add_response(json=sample_flight_data)
    client = FlightStatusClient("http://localhost:5001")
    flights = await client.get_flights(airport="BDL")
    assert len(flights) == 1
    assert flights[0].flight_number == "DL1234"
    assert flights[0].airport == "BDL"


@pytest.mark.asyncio
async def test_get_flights_empty(httpx_mock):
    httpx_mock.add_response(json=[])
    client = FlightStatusClient("http://localhost:5001")
    flights = await client.get_flights(airport="ZZZ")
    assert flights == []


@pytest.mark.asyncio
async def test_get_flights_filters_empty_params(httpx_mock, sample_flight_data):
    httpx_mock.add_response(json=sample_flight_data)
    client = FlightStatusClient("http://localhost:5001")
    await client.get_flights(airport="BDL", flight_number="", time="")
    request = httpx_mock.get_request()
    assert "flightNumber" not in str(request.url)
    assert "time" not in str(request.url)
