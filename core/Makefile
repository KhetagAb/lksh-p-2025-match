.DEFAULT_GOAL := quickstart

include .env
export
mode := dev

quickstart: check
	make build mode=dev
	make start mode=dev
	make clean mode=dev

build: check
	go mod tidy
	go build -o bin/match cmd/main.go

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

migrate:
	go run github.com/pressly/goose/v3/cmd/goose -dir migrations postgres postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_EXPOSED_PORT}/${POSTGRES_DB} up

codegen:
# TODO:issue
	go tool github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen --config config/openapi.yaml ../docs/api/openapi.yaml
	rm -rf internal/generated/wireset/
	mkdir -p internal/generated/wireset
	go tool github.com/google/wire/cmd/wire ./cmd/wireset
	mv cmd/wireset/wire_gen.go internal/generated/wireset

run-local:
	bin/match

test-local:
	go test

check: # need to have golangci-lint installed
	golangci-lint run

clean: # have to be root sometimes
	rm -rf bin/ db
