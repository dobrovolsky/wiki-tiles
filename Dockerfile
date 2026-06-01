FROM python:3.14-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y \
    lbzip2 \
    pv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
