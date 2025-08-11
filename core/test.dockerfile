FROM golang:1.23.8

COPY .. /app
WORKDIR /app

CMD ["go", "test"]

EXPOSE 8080
