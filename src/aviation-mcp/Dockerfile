FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files first (layer caching)
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --no-dev

# Copy source code
COPY src/ src/

# Ensure src package is importable
ENV PYTHONPATH=/app

# Expose MCP SSE port
EXPOSE 8000

# Start MCP server
ENTRYPOINT ["uv", "run", "src/server.py"]
