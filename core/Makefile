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

start-local:
	sh migrations/upgrade.sh
	bin/match

test-local: codegen
	go test

codegen:
	go tool github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen --config config/openapi.yaml ../docs/api/openapi.yaml
	go tool github.com/google/wire/cmd/wire ./cmd/wireset
	mv ./cmd/wireset/wire_gen.go ./internal/generated

check: # need to have golangci-lint installed
	golangci-lint run

clean: # have to be root sometimes
	rm -rf bin/ db
