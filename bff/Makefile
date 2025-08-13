codegen:
	openapi-python-client generate --path ../docs/api/openapi.yaml --overwrite --output-path .

up:
	docker-compose -f docker-compose.yml up --build --force-recreate --remove-orphans -d

down:
	docker-compose -f docker-compose.yml down -v