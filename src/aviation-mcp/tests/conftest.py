import pytest

from src.config import Config


@pytest.fixture
def config():
    """Config with localhost URLs for testing."""
    return Config()


@pytest.fixture
def sample_flight_data():
    """Sample flight JSON matching C# service response."""
    return [
        {
            "airport": "BDL",
            "flightNumber": "DL1234",
            "airline": "Delta",
            "origin": "BDL",
            "destination": "ATL",
            "departureTime": "2026-02-09T14:30:00Z",
            "arrivalTime": "2026-02-09T17:45:00Z",
            "status": "On Time",
            "gate": "A12",
            "terminal": "Terminal A",
        }
    ]


@pytest.fixture
def sample_gate_data():
    """Sample gate JSON matching C# service response."""
    return [
        {
            "airport": "BDL",
            "gateNumber": "A1",
            "terminal": "Terminal A",
            "status": "Boarding",
            "assignedFlight": "DL1234",
            "airline": "Delta",
            "lastUpdated": "2026-02-09T14:00:00Z",
        }
    ]


@pytest.fixture
def sample_weather_data():
    """Sample weather JSON matching C# service response."""
    return [
        {
            "airport": "BDL",
            "condition": "Clear",
            "temperatureF": 28.0,
            "temperatureC": -2.2,
            "windSpeed": "10 mph NW",
            "visibility": "10 miles",
            "humidity": 45,
            "lastUpdated": "2026-02-09T12:00:00Z",
        }
    ]
