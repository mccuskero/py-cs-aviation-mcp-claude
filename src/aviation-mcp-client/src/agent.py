from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from src.config import Config


def build_mcp_client(config: Config) -> MultiServerMCPClient:
    """Create a MultiServerMCPClient configured for the aviation MCP server."""
    return MultiServerMCPClient(
        {
            "aviation-mcp": {
                "url": config.mcp_url,
                "transport": "sse",
            }
        }
    )


async def run_interactive(config: Config):
    """Run the interactive REPL within the MCP client context.

    The agent and tools are only valid inside the async with block,
    so the REPL loop must run here.
    """
    client = build_mcp_client(config)
    async with client as c:
        tools = await c.get_tools()
        model = config.get_chat_model()
        agent = create_react_agent(model, tools)

        print("Aviation MCP Client (type 'quit' to exit)")
        print(f"Connected to MCP server at {config.mcp_url}")
        print(f"Tools available: {[t.name for t in tools]}")
        print()

        while True:
            try:
                query = input("> ")
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break

            if query.strip().lower() in ("quit", "exit"):
                print("Goodbye!")
                break
            if not query.strip():
                continue

            result = await agent.ainvoke({"messages": [("user", query)]})
            print(result["messages"][-1].content)
            print()
