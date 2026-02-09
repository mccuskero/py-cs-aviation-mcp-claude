from unittest.mock import AsyncMock, patch

import httpx
import pytest

from src.models.flight import Flight
from src.tools.flight_status import FlightStatusTool


@pytest.mark.asyncio
async def test_execute_returns_formatted_string(config):
    tool = FlightStatusTool(config)
    mock_flights = [
        Flight(
            airport="BDL",
            flight_number="DL1234",
            airline="Delta",
            origin="BDL",
            destination="ATL",
            departure_time="2026-02-09T14:30:00Z",
            arrival_time="2026-02-09T17:45:00Z",
            status="On Time",
            gate="A12",
            terminal="Terminal A",
        )
    ]
    with patch.object(tool.client, "get_flights", new_callable=AsyncMock, return_value=mock_flights):
        result = await tool.execute(airport="BDL")
    assert "DL1234" in result
    assert "Delta" in result
    assert "On Time" in result


@pytest.mark.asyncio
async def test_execute_no_results(config):
    tool = FlightStatusTool(config)
    with patch.object(tool.client, "get_flights", new_callable=AsyncMock, return_value=[]):
        result = await tool.execute(airport="ZZZ")
    assert "No flights found" in result


@pytest.mark.asyncio
async def test_execute_service_unavailable(config):
    tool = FlightStatusTool(config)
    with patch.object(
        tool.client, "get_flights", new_callable=AsyncMock, side_effect=httpx.ConnectError("")
    ):
        result = await tool.execute(airport="BDL")
    assert "Error" in result
    assert "unavailable" in result
