FROM golang:1.24.6 AS builder

WORKDIR /app

COPY core/go.mod core/go.sum ./

RUN go mod download

COPY core/ .
COPY docs/api/openapi.yaml ../docs/api/openapi.yaml

RUN make build-local
CMD ["make", "start-local"]


FROM alpine:latest

RUN apk --no-cache add ca-certificates
WORKDIR /root/

COPY --from=builder /app/bin/match .

CMD ["./match"]

EXPOSE 8080
