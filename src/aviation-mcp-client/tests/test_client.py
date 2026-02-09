from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.config import Config
from src.test_runner import TEST_SCENARIOS, TestScenario, check_result, run_batch_tests


# --- Config tests ---


class TestConfig:
    def test_defaults(self):
        config = Config()
        assert config.mcp_url == "http://localhost:8000/sse"
        assert config.llm_provider == "anthropic"
        assert config.llm_model == "claude-sonnet-4-5-20250929"

    def test_env_override(self, monkeypatch):
        monkeypatch.setenv("MCP_SERVER_URL", "http://custom:9000/sse")
        monkeypatch.setenv("LLM_PROVIDER", "openai")
        config = Config()
        assert config.mcp_url == "http://custom:9000/sse"
        assert config.llm_provider == "openai"

    def test_get_chat_model_anthropic(self):
        config = Config(llm_provider="anthropic", llm_api_key="test-key")
        with patch("langchain_anthropic.ChatAnthropic") as mock_cls:
            config.get_chat_model()
            mock_cls.assert_called_once_with(
                model="claude-sonnet-4-5-20250929", api_key="test-key"
            )

    def test_get_chat_model_unsupported(self):
        config = Config(llm_provider="unsupported")
        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            config.get_chat_model()

    def test_get_chat_model_no_api_key(self):
        config = Config(llm_provider="anthropic", llm_api_key="")
        with patch("langchain_anthropic.ChatAnthropic") as mock_cls:
            config.get_chat_model()
            mock_cls.assert_called_once_with(model="claude-sonnet-4-5-20250929")

    def test_get_chat_model_ollama_defaults(self):
        config = Config(llm_provider="ollama", llm_model="llama3.2")
        with patch("langchain_openai.ChatOpenAI") as mock_cls:
            config.get_chat_model()
            mock_cls.assert_called_once_with(
                model="llama3.2",
                base_url="http://localhost:11434/v1",
                api_key="ollama",
            )

    def test_get_chat_model_ollama_custom_url(self):
        config = Config(
            llm_provider="ollama",
            llm_model="mistral",
            llm_base_url="http://myhost:11434/v1",
        )
        with patch("langchain_openai.ChatOpenAI") as mock_cls:
            config.get_chat_model()
            mock_cls.assert_called_once_with(
                model="mistral",
                base_url="http://myhost:11434/v1",
                api_key="ollama",
            )

    def test_get_chat_model_openai_with_base_url(self):
        config = Config(
            llm_provider="openai",
            llm_model="gpt-4o",
            llm_api_key="sk-test",
            llm_base_url="https://custom-endpoint.example.com/v1",
        )
        with patch("langchain_openai.ChatOpenAI") as mock_cls:
            config.get_chat_model()
            mock_cls.assert_called_once_with(
                model="gpt-4o",
                api_key="sk-test",
                base_url="https://custom-endpoint.example.com/v1",
            )


# --- TestScenario tests ---


class TestTestScenario:
    def test_scenario_creation(self):
        scenario = TestScenario("test", "get_flight_status", {"airport": "BDL"}, "non_empty")
        assert scenario.name == "test"
        assert scenario.tool_name == "get_flight_status"
        assert scenario.params == {"airport": "BDL"}
        assert scenario.expected_check == "non_empty"

    def test_scenarios_cover_all_tools(self):
        tool_names = {s.tool_name for s in TEST_SCENARIOS}
        assert tool_names == {"get_flight_status", "get_gate_info", "get_weather"}

    def test_scenarios_count(self):
        assert len(TEST_SCENARIOS) == 8


# --- check_result tests ---


def _mock_result(text: str) -> MagicMock:
    """Create a mock CallToolResult with the given text content."""
    content_item = MagicMock()
    content_item.text = text
    result = MagicMock()
    result.content = [content_item]
    return result


class TestCheckResult:
    def test_non_empty_with_flight_data(self):
        result = _mock_result(
            "Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12"
        )
        scenario = TestScenario("test", "tool", {}, "non_empty")
        assert check_result(result, scenario) is True

    def test_non_empty_with_gate_data(self):
        result = _mock_result(
            "Gate C22 (C): Status: Boarding, Flight: DL400, Airline: Delta"
        )
        scenario = TestScenario("test", "tool", {}, "non_empty")
        assert check_result(result, scenario) is True

    def test_non_empty_with_weather_data(self):
        result = _mock_result(
            "LAX: Clear, 68.0°F / 20.0°C, Wind: 5 mph W, Visibility: 10 miles, Humidity: 40%"
        )
        scenario = TestScenario("test", "tool", {}, "non_empty")
        assert check_result(result, scenario) is True

    def test_empty_no_flights(self):
        result = _mock_result("No flights found matching the criteria.")
        scenario = TestScenario("test", "tool", {}, "empty")
        assert check_result(result, scenario) is True

    def test_empty_no_gates(self):
        result = _mock_result("No gate information found matching the criteria.")
        scenario = TestScenario("test", "tool", {}, "empty")
        assert check_result(result, scenario) is True

    def test_empty_no_weather(self):
        result = _mock_result("No weather data found for the specified airport.")
        scenario = TestScenario("test", "tool", {}, "empty")
        assert check_result(result, scenario) is True

    def test_non_empty_fails_when_no_data(self):
        result = _mock_result("No flights found matching the criteria.")
        scenario = TestScenario("test", "tool", {}, "non_empty")
        assert check_result(result, scenario) is False

    def test_empty_fails_when_data_present(self):
        result = _mock_result(
            "Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12"
        )
        scenario = TestScenario("test", "tool", {}, "empty")
        assert check_result(result, scenario) is False

    def test_empty_content_list(self):
        result = MagicMock()
        result.content = []
        scenario = TestScenario("test", "tool", {}, "empty")
        assert check_result(result, scenario) is True


# --- run_batch_tests tests (mocked MCP session) ---


class TestRunBatchTests:
    @pytest.mark.asyncio
    async def test_all_pass(self):
        """All scenarios pass when MCP returns appropriate data."""
        mock_session = AsyncMock()
        mock_session.initialize = AsyncMock()

        # Return formatted text for positive tests, "No ... found" for negative tests
        async def mock_call_tool(tool_name, params):
            airport = params.get("airport", "")
            gate_number = params.get("gate_number", "")
            if airport == "XXX":
                if "flight" in tool_name:
                    return _mock_result("No flights found matching the criteria.")
                return _mock_result("No weather data found for the specified airport.")
            if gate_number == "Z99":
                return _mock_result("No gate information found matching the criteria.")
            return _mock_result("Flight DL1234 (Delta): BDL -> ATL, Status: On Time")

        mock_session.call_tool = AsyncMock(side_effect=mock_call_tool)

        # Mock the sse_client and ClientSession context managers
        mock_sse = AsyncMock()
        mock_sse.__aenter__ = AsyncMock(return_value=(MagicMock(), MagicMock()))
        mock_sse.__aexit__ = AsyncMock(return_value=False)

        with (
            patch("src.test_runner.sse_client", return_value=mock_sse),
            patch("src.test_runner.ClientSession", return_value=mock_session),
        ):
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=False)

            config = Config(mcp_url="http://test:8000/sse")
            result = await run_batch_tests(config)
            assert result is True

    @pytest.mark.asyncio
    async def test_failure_detected(self):
        """Batch runner detects failures when results don't match expectations."""
        mock_session = AsyncMock()
        mock_session.initialize = AsyncMock()
        # Return "no data" for all calls — positive tests will fail
        mock_session.call_tool = AsyncMock(
            return_value=_mock_result("No flights found matching the criteria.")
        )

        mock_sse = AsyncMock()
        mock_sse.__aenter__ = AsyncMock(return_value=(MagicMock(), MagicMock()))
        mock_sse.__aexit__ = AsyncMock(return_value=False)

        with (
            patch("src.test_runner.sse_client", return_value=mock_sse),
            patch("src.test_runner.ClientSession", return_value=mock_session),
        ):
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=False)

            config = Config(mcp_url="http://test:8000/sse")
            result = await run_batch_tests(config)
            assert result is False
