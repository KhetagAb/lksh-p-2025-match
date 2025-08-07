FROM golang:1.23.8

COPY . /app
WORKDIR /app

RUN go build -o bin/match cmd/main.go

CMD ["bin/match"]

EXPOSE 8080
