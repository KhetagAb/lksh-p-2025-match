#!/usr/bin/bash

# only call from core
$(go env GOPATH)/bin/goose \
  -dir migrations \
  postgres "host=${POSTGRES_HOST} port=${POSTGRES_PORT} user=${POSTGRES_USER} password=${POSTGRES_PASSWORD} dbname=${POSTGRES_DB} sslmode=disable" \
  up
