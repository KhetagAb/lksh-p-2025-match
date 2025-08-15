#!/usr/bin/bash

# only call from core/
goose -dir migrations postgres postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_EXPOSED_PORT}/${POSTGRES_DB} up
