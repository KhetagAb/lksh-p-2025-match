FROM golang:1.24.6

COPY . /app
WORKDIR /app

RUN go mod tidy
RUN make codegen
RUN go build -o bin/match cmd/main.go

CMD ["bin/match"]

EXPOSE 8080
