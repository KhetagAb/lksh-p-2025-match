FROM golang:1.24.6 AS builder

WORKDIR /app

COPY core/go.mod core/go.sum ./

RUN go mod download

COPY core/ .
COPY docs/api/openapi.yaml ./openapi.yaml

RUN make migrate
RUN make codegen
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o bin/match cmd/main.go

FROM alpine:latest

RUN apk --no-cache add ca-certificates
WORKDIR /root/

COPY --from=builder /app/bin/match .

CMD ["./match"]

EXPOSE 8080
