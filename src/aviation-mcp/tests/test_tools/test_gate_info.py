from unittest.mock import AsyncMock, patch

import httpx
import pytest

from src.models.gate import Gate
from src.tools.gate_info import GateInfoTool


@pytest.mark.asyncio
async def test_execute_returns_formatted_string(config):
    tool = GateInfoTool(config)
    mock_gates = [
        Gate(
            airport="BDL",
            gate_number="A1",
            terminal="Terminal A",
            status="Boarding",
            assigned_flight="DL1234",
            airline="Delta",
            last_updated="2026-02-09T14:00:00Z",
        )
    ]
    with patch.object(tool.client, "get_gates", new_callable=AsyncMock, return_value=mock_gates):
        result = await tool.execute(airport="BDL")
    assert "A1" in result
    assert "Boarding" in result
    assert "DL1234" in result


@pytest.mark.asyncio
async def test_execute_no_results(config):
    tool = GateInfoTool(config)
    with patch.object(tool.client, "get_gates", new_callable=AsyncMock, return_value=[]):
        result = await tool.execute(airport="ZZZ")
    assert "No gate information found" in result


@pytest.mark.asyncio
async def test_execute_service_unavailable(config):
    tool = GateInfoTool(config)
    with patch.object(
        tool.client, "get_gates", new_callable=AsyncMock, side_effect=httpx.ConnectError("")
    ):
        result = await tool.execute(airport="BDL")
    assert "Error" in result
    assert "unavailable" in result
