.DEFAULT_GOAL := quickstart
mode := dev


quickstart: check
	make build mode=dev
	make start mode=dev
	make clean mode=dev

codegen:
	go tool github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen --config config/openapi.yaml ../docs/api/openapi.yaml
	go tool github.com/google/wire/cmd/wire ./cmd/wireset
	mkdir ./internal/generated/app/
	mv ./cmd/wireset/wire_gen.go ./internal/generated/app

start:
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans

up:
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans -d

test:
	docker-compose -f docker-compose.test.yml up --build --force-recreate --remove-orphans --abort-on-container-exit

stop:
	docker-compose -f docker-compose.$(mode).yml stop

rm:
	docker-compose -f docker-compose.$(mode).yml stop

build-local: codegen
	go build -o bin/match cmd/main.go

start-local:
	sh migrations/upgrade.sh
	bin/match

test-local: codegen
	go test

check:
	golangci-lint run

clean:
	rm -rf bin/ db
