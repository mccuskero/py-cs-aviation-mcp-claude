from abc import ABC, abstractmethod

from src.config import Config


class BaseTool(ABC):
    """Base class for MCP tool handlers."""

    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Execute the tool and return a formatted string result."""
        ...
