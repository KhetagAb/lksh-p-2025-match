.DEFAULT_GOAL := quickstart
mode := dev


quickstart: check
	make build mode=dev
	make start mode=dev
	make clean mode=dev

codegen:
	go tool github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen --config config/openapi.yaml ../docs/api/openapi.yaml
	go tool github.com/google/wire/cmd/wire ./cmd/wireset
	mv ./cmd/wireset/wire_gen.go ./internal/generated

build: codegen
	go build -o bin/match cmd/main.go

start:
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans

up:
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans -d

stop:
	docker-compose -f docker-compose.$(mode).yml stop

down:
	docker-compose -f docker-compose.$(mode).yml down -v

start-migrate:
	sh migrations/upgrade.sh
	bin/match

test: codegen
	go test

check:
	golangci-lint run

clean:
	rm -rf bin/ db
