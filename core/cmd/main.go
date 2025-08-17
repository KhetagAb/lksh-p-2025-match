package main

import (
	"context"
	"fmt"
	"github.com/labstack/echo/v4"
	"log"
	"match/internal/application/transport"
	"match/internal/generated/app"
	"match/internal/infra"
	"net/http"
	"os/signal"
	"sync/atomic"
	"syscall"
	"time"
)

const (
	_shutdownPeriod      = 15 * time.Second
	_shutdownHardPeriod  = 3 * time.Second
	_readinessDrainDelay = 5 * time.Second
)

var isShuttingDown atomic.Bool

func main() {
	infra.Init()
	svc, err := wireset.InitializeApp()
	if err != nil {
		panic(fmt.Sprintf("failed to initialize server: %v", err))
	}

	server := svc.HttpServer
	server.RegisterHealthCheck(Healthcheck)
	go func() {
		if err := server.StartServer(); err != nil {
			infra.Errorf(svc.Ctx, "failed to start http server: %v", err)
		}
	}()

	rootCtx, _ := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	awaitGracefulShutdown(rootCtx, server)
}

func Healthcheck(c echo.Context) error {
	if isShuttingDown.Load() {
		return c.String(http.StatusServiceUnavailable, "Shutting down")
	}
	return c.String(http.StatusOK, "OK")
}

func awaitGracefulShutdown(ctx context.Context, server *transport.HTTPServer) {
	<-ctx.Done()
	isShuttingDown.Store(true)
	log.Println("Received shutdown signal, shutting down.")

	// Give time for readiness check to propagate
	time.Sleep(_readinessDrainDelay)
	log.Println("Readiness check propagated, now waiting for ongoing requests to finish.")

	shutdownCtx, cancel := context.WithTimeout(context.Background(), _shutdownPeriod)
	defer cancel()

	err := server.StopServer(shutdownCtx)
	if err != nil {
		log.Println("Failed to wait for ongoing requests to finish, waiting for forced cancellation.")
		time.Sleep(_shutdownHardPeriod)
	}

	log.Println("Server shut down gracefully.")
}
