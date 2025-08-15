FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app

COPY bff/pyproject.toml ./app/bff/

ENV UV_COMPILE_BYTECODE 0
ENV UV_LINK_MODE=copy
ENV PATH="/.venv/bin:$PATH"

RUN uv venv --python 3.13.5
    uv sync

COPY ./bff ./app/bff
COPY ./docs/openapi.yaml ./app/docs/openapi.yaml

RUN uv run openapi-python-client generate --path ./docs/api/openapi.yaml --overwrite --output-path bff/

ENTRYPOINT []

CMD ["python", "lkshmatch.main.py"]
