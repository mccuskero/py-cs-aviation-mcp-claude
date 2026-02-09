import pytest

from src.clients.gate_info_client import GateInfoClient


@pytest.mark.asyncio
async def test_get_gates_success(httpx_mock, sample_gate_data):
    httpx_mock.add_response(json=sample_gate_data)
    client = GateInfoClient("http://localhost:5002")
    gates = await client.get_gates(airport="BDL")
    assert len(gates) == 1
    assert gates[0].gate_number == "A1"
    assert gates[0].airport == "BDL"


@pytest.mark.asyncio
async def test_get_gates_empty(httpx_mock):
    httpx_mock.add_response(json=[])
    client = GateInfoClient("http://localhost:5002")
    gates = await client.get_gates(airport="ZZZ")
    assert gates == []


@pytest.mark.asyncio
async def test_get_gates_filters_empty_params(httpx_mock, sample_gate_data):
    httpx_mock.add_response(json=sample_gate_data)
    client = GateInfoClient("http://localhost:5002")
    await client.get_gates(airport="BDL", gate_number="")
    request = httpx_mock.get_request()
    assert "gateNumber" not in str(request.url)
