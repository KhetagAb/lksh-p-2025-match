.DEFAULT_GOAL := start
mode := dev

codegen:
	go generate ./cmd

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

build: codegen
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
