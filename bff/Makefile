.DEFAULT_GOAL = start
mode := dev

check: lint typecheck

codegen:
	uv run openapi-python-client generate --path ../docs/api/openapi.yaml --overwrite --output-path lkshmatch/

up:
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans -d

start:
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans

stop:
	docker-compose -f docker-compose.$(mode).yml stop

rm:
	docker-compose -f docker-compose.$(mode).yml rm
	rm -rf .venv

lint:
	uv run ruff check lkshmatch

typecheck:
	uv run mypy -p lkshmatch --config-file=pyproject.toml

venv:
	uv venv --python 3.13.5
	uv sync
