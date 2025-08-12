.DEFAULT_GOAL := quickstart

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
	docker-compose -f docker-compose.$(mode).yml stop --build --force-recreate --remove-orphans -d

test:
	docker-compose -f docker-compose.test.yml --build --force-recreate --remove-orphans --abort-on-container-exit

upgrade:
	go tool github.com/pressly/goose/v3/cmd/goose -dir migrations postgres $(uri) up

codegen:
	go tool github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen --config api/config.yaml api/openapi.yaml
	cd internal/generated/app && go tool github.com/google/wire/cmd/wire .

run-local:
	bin/match

test-local:
	go test

check: # need to have golangci-lint installed
	golangci-lint run

clean: # have to be root sometimes
	rm -rf bin/ db
