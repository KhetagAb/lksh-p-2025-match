FROM golang:1.24.6

WORKDIR /app

COPY core/go.mod core/go.sum ./

RUN go mod download

COPY core/ .
COPY docs/api/openapi.yaml ../docs/api/openapi.yaml

RUN make migrate
RUN make codegen
RUN go build -o bin/match cmd/main.go

CMD ["bin/match"]

EXPOSE 8080
