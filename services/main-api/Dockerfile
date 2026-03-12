FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock /app/
WORKDIR /app
ENV UV_NO_DEV=1
RUN uv sync --locked

COPY . /app

CMD ["uv", "run", "main.py"]