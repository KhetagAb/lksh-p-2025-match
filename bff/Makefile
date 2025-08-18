.DEFAULT_GOAL = start
mode := dev

check: lint typecheck

# FIXME переработат, учесть dev.dockefile
codegen:
	uv run openapi-python-client generate --path ../docs/api/openapi.yaml --overwrite --output-path ./tmp
	rm -rf core_client
	mv tmp/core_client core_client
	rm -rf ./tmp

up:
	docker compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans -d

start:
	docker compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans

stop:
	docker-compose -f docker-compose.$(mode).yml stop

down:
	docker-compose -f docker-compose.$(mode).yml down -v

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
