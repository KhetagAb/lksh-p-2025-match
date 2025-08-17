FROM golang:1.24.6

WORKDIR /app

COPY core/go.mod core/go.sum ./
RUN go mod tidy

COPY core/ .
COPY docs/api/openapi.yaml ../docs/api/openapi.yaml

CMD ["make", "test"]

EXPOSE 8080
