import os


class Config:
    """Server configuration loaded from environment variables."""

    def __init__(self):
        self.flight_status_url: str = os.getenv(
            "FLIGHT_STATUS_URL", "http://localhost:5001"
        )
        self.gate_info_url: str = os.getenv(
            "GATE_INFO_URL", "http://localhost:5002"
        )
        self.weather_url: str = os.getenv(
            "WEATHER_URL", "http://localhost:5003"
        )
        self.debug: bool = os.getenv("MCP_DEBUG", "false").lower() == "true"
