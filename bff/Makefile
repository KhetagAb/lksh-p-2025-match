check: lint typecheck

codegen:
	openapi-python-client generate --path ../docs/api/openapi.yaml --overwrite --output-path .

up:
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans -d

start:
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans

stop:
	docker-compose -f docker-compose.$(mode).yml stop -v

lint:
	uv run ruff check lkshmatch

typecheck:
	uv run mypy -p lkshmatch --config-file=pyproject.toml

venv:
	uv venv --python 3.13.5
	uv sync
