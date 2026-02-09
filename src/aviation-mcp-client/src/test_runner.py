import json
from dataclasses import dataclass

from mcp import ClientSession
from mcp.client.sse import sse_client

from src.config import Config


@dataclass
class TestScenario:
    name: str
    tool_name: str
    params: dict
    expected_check: str  # "non_empty" or "empty"


TEST_SCENARIOS = [
    # Flight status tests
    TestScenario(
        "Flight lookup at BDL", "get_flight_status", {"airport": "BDL"}, "non_empty"
    ),
    TestScenario(
        "Flight by number",
        "get_flight_status",
        {"airport": "BDL", "flight_number": "DL1234"},
        "non_empty",
    ),
    TestScenario(
        "Unknown airport returns empty",
        "get_flight_status",
        {"airport": "XXX"},
        "empty",
    ),
    # Gate info tests
    TestScenario("Gates at JFK", "get_gate_info", {"airport": "JFK"}, "non_empty"),
    TestScenario(
        "Specific gate", "get_gate_info", {"airport": "BDL", "gate_number": "A1"}, "non_empty"
    ),
    TestScenario(
        "Unknown gate returns empty",
        "get_gate_info",
        {"airport": "JFK", "gate_number": "Z99"},
        "empty",
    ),
    # Weather tests
    TestScenario("Weather at LAX", "get_weather", {"airport": "LAX"}, "non_empty"),
    TestScenario(
        "Unknown airport weather", "get_weather", {"airport": "XXX"}, "empty"
    ),
]


def check_result(result, scenario: TestScenario) -> bool:
    """Validate a tool call result against the expected check."""
    try:
        # MCP CallToolResult has .content which is a list of TextContent
        if not result.content:
            text = "[]"
        else:
            text = result.content[0].text

        data = json.loads(text)

        if scenario.expected_check == "non_empty":
            if isinstance(data, list):
                return len(data) > 0
            return bool(data)
        elif scenario.expected_check == "empty":
            if isinstance(data, list):
                return len(data) == 0
            return not data
        else:
            return False
    except (json.JSONDecodeError, IndexError, AttributeError):
        return False


async def run_batch_tests(config: Config) -> bool:
    """Run all batch test scenarios against the MCP server.

    Connects directly via SSE (no LLM required).
    Returns True if all scenarios pass, False otherwise.
    """
    print(f"Connecting to MCP server at {config.mcp_url}...")
    print()

    async with sse_client(config.mcp_url) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            passed_count = 0
            total = len(TEST_SCENARIOS)

            for scenario in TEST_SCENARIOS:
                try:
                    result = await session.call_tool(
                        scenario.tool_name, scenario.params
                    )
                    passed = check_result(result, scenario)
                except Exception as e:
                    print(f"  [FAIL] {scenario.name} — error: {e}")
                    continue

                status = "PASS" if passed else "FAIL"
                print(f"  [{status}] {scenario.name}")
                if passed:
                    passed_count += 1

            print()
            print(f"Results: {passed_count}/{total} passed")
            return passed_count == total
