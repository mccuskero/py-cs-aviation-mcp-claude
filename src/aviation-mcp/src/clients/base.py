import logging

import httpx

logger = logging.getLogger(__name__)


class BaseServiceClient:
    """Base HTTP client for C# microservice communication."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get(self, path: str, params: dict) -> list[dict]:
        """Send GET request with filtered params, return JSON response."""
        filtered = {k: v for k, v in params.items() if v}
        async with httpx.AsyncClient() as client:
            logger.debug("GET %s%s params=%s", self.base_url, path, filtered)
            response = await client.get(
                f"{self.base_url}{path}",
                params=filtered,
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
