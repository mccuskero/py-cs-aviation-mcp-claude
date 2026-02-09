import logging
import sys


def setup_protocol_logging() -> None:
    """Enable protocol-level debug logging for MCP and HTTP communication.

    Configures Python logging to capture:
    - MCP SDK JSON-RPC messages (tool registration, capability negotiation)
    - HTTP request/response details to C# services
    """
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # MCP SDK loggers
    for logger_name in ("mcp", "mcp.server", "mcp.server.fastmcp"):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    # HTTP client logging
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.DEBUG)
    httpx_logger.addHandler(handler)

    # Application logging
    app_logger = logging.getLogger("aviation_mcp")
    app_logger.setLevel(logging.DEBUG)
    app_logger.addHandler(handler)

    app_logger.info("Protocol debug logging enabled")
