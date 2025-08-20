FROM golang:1.24.6

WORKDIR /app

COPY core/go.mod core/go.sum ./
RUN go mod download

RUN go install -tags='no_clickhouse no_libsql no_mssql no_mysql no_sqlite3 no_vertica no_ydb' github.com/pressly/goose/v3/cmd/goose

COPY core/ .
COPY docs/api/openapi.yaml ../docs/api/openapi.yaml

RUN make build

CMD ["make", "start-local"]

EXPOSE 8080
