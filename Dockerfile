FROM python:3.13.3-slim-bullseye

COPY --from=ghcr.io/astral-sh/uv:0.6.17 /uv /uvx /bin/
COPY . /app

WORKDIR /app
RUN uv sync --frozen

ENTRYPOINT ["scripts/entrypoint.sh"]
