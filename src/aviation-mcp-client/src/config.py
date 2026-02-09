import os
from dataclasses import dataclass, field


@dataclass
class Config:
    mcp_url: str = field(
        default_factory=lambda: os.getenv("MCP_SERVER_URL", "http://localhost:8000/sse")
    )
    llm_provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "anthropic"))
    llm_model: str = field(
        default_factory=lambda: os.getenv("LLM_MODEL", "claude-sonnet-4-5-20250929")
    )
    llm_api_key: str = field(default_factory=lambda: os.getenv("LLM_API_KEY", ""))
    llm_base_url: str = field(default_factory=lambda: os.getenv("LLM_BASE_URL", ""))

    def get_chat_model(self):
        if self.llm_provider == "anthropic":
            from langchain_anthropic import ChatAnthropic

            kwargs = {"model": self.llm_model}
            if self.llm_api_key:
                kwargs["api_key"] = self.llm_api_key
            return ChatAnthropic(**kwargs)
        elif self.llm_provider == "openai":
            from langchain_openai import ChatOpenAI

            kwargs = {"model": self.llm_model}
            if self.llm_api_key:
                kwargs["api_key"] = self.llm_api_key
            if self.llm_base_url:
                kwargs["base_url"] = self.llm_base_url
            return ChatOpenAI(**kwargs)
        elif self.llm_provider == "ollama":
            from langchain_openai import ChatOpenAI

            base_url = self.llm_base_url or "http://localhost:11434/v1"
            return ChatOpenAI(
                model=self.llm_model,
                base_url=base_url,
                api_key="ollama",
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")
