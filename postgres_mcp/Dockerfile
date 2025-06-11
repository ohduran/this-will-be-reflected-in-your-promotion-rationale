FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc libpq-dev curl && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app
COPY . /app

RUN uv venv && \
    uv pip install "mcp[cli]" asyncpg

CMD ["uv", "run", "main.py"] 