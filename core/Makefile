.DEFAULT_GOAL := quickstart

quickstart: check
	make build mode=dev
	make start mode=dev
	make clean mode=dev

build: check
	go mod tidy
	go build -o bin/match cmd/main.go

start: check
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans

up: check
	docker-compose -f docker-compose.$(mode).yml up --build --force-recreate --remove-orphans -d

test: check
	docker-compose -f docker-compose.test.yml --build --force-recreate --remove-orphans --abort-on-container-exit

run-local:
	bin/match

test-local:
	go test

check: # need to have golangci-lint installed
	golangci-lint run

clean: # have to be root sometimes
	rm -rf bin/ db
