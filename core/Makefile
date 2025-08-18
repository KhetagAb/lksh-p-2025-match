.DEFAULT_GOAL := start
mode := dev

codegen:
	go tool github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen --config config/openapi.yaml ../docs/api/openapi.yaml
	go tool github.com/google/wire/cmd/wire ./cmd/wireset
	mv ./cmd/wireset/wire_gen.go ./internal/generated/wire_gen.go

start:
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans

up:
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans -d

test:
	docker-compose -f docker-compose.test.yml up --build --force-recreate --remove-orphans --abort-on-container-exit

stop:
	docker-compose -f docker-compose.$(mode).yml stop

down:
	docker-compose -f docker-compose.$(mode).yml down -v

rm:
	docker-compose -f docker-compose.$(mode).yml rm
	rm -rf internal/generated/* db/

build-local:
	go build -o bin/match cmd/main.go

start-local:
	sh migrations/upgrade.sh
	bin/match

test-local:
	sh migrations/upgrade.sh
	go test ./...

check:
	golangci-lint run

clean:
	rm -rf bin/ db
