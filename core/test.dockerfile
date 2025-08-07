FROM golang:1.23.8

COPY .. /app
WORKDIR /app

CMD ["go", "build"]

EXPOSE 8080
