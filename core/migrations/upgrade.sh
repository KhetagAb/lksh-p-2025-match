#!/usr/bin/bash

# only call from core
$(go env GOPATH)/bin/goose \
  -dir migrations \
  postgres "host=${APP_POSTGRES_HOST} port=${APP_POSTGRES_PORT} user=${APP_POSTGRES_USER} password=${APP_POSTGRES_PASSWORD} dbname=${APP_POSTGRES_DATABASE} sslmode=disable" \
  up
