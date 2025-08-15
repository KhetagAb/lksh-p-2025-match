FROM golang:1.24.6

WORKDIR /app

COPY core/go.mod core/go.sum ./

RUN go mod download

COPY core/ .
COPY docs/api/openapi.yaml ../docs/api/openapi.yaml

RUN make build

CMD ["make", "start-migrate"]

EXPOSE 8080
