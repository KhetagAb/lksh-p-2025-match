package main

import (
	"log/slog"

	"match/internal/transport"
)

func main() {
	server := transport.GetServer()
	transport.RunServer(server)
	awaitGracefulShutdown()

}

func awaitGracefulShutdown() {
	slog.Info("shutting down server...")
	// TODO: shut down database transactions & maybe wait a lil bit?
}
