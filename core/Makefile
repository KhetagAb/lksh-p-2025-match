.DEFAULT_GOAL := quickstart
mode := dev

quickstart: check
	make build mode=dev
	make start mode=dev
	make clean mode=dev

start:
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans

up:
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans -d

stop:
	docker-compose -f docker-compose.$(mode).yml stop

down:
	docker-compose -f docker-compose.$(mode).yml down -v

test:
	docker-compose -f docker-compose.test.yml --build --force-recreate --remove-orphans --abort-on-container-exit

build-local: codegen check
	go build -o bin/match cmd/main.go

start-local: upgrade
	bin/match

test-local: codegen
	go test

upgrade:
	goose -dir migrations postgres postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_EXPOSED_PORT}/${POSTGRES_DB} up

codegen:
	go tool github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen --config api/config.yaml ../docs/api/openapi.yaml
	cd internal/generated/app && go tool github.com/google/wire/cmd/wire .

check: # need to have golangci-lint installed
	golangci-lint run

clean: # have to be root sometimes
	rm -rf bin/ db
