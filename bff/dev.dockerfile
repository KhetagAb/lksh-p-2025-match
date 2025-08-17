FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app

COPY bff/pyproject.toml .

ENV UV_COMPILE_BYTECODE 0
ENV UV_LINK_MODE=copy
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

RUN uv venv --python 3.13.5 && \
    uv sync

COPY ./bff .
COPY ./docs/api/openapi.yaml ../docs/api/openapi.yaml

RUN make codegen

ENTRYPOINT []

CMD ["uv", "run", "python", "-m", "lkshmatch.main"]
