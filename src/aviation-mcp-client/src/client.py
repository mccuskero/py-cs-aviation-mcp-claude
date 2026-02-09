import argparse
import asyncio

from src.agent import run_interactive
from src.config import Config
from src.test_runner import run_batch_tests


async def main():
    parser = argparse.ArgumentParser(description="Aviation MCP Test Client")
    parser.add_argument("--test", action="store_true", help="Run batch tests (no LLM required)")
    parser.add_argument("--mcp-url", default=None, help="MCP server SSE URL")
    args = parser.parse_args()

    config = Config()
    if args.mcp_url:
        config.mcp_url = args.mcp_url

    if args.test:
        success = await run_batch_tests(config)
        raise SystemExit(0 if success else 1)
    else:
        await run_interactive(config)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
