package main

import (
	"fmt"
	"match/internal/generated/app"
	"match/pkg/logger"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	logger.Init()
	svc, err := app.InitializeApp()
	if err != nil {
		panic(fmt.Sprintf("failed to initialize server: %v", err))
	}

	server := svc.HttpServer
	go func() {
		if err := server.StartServer(); err != nil {
			logger.Errorf(svc.Ctx, "failed to start http server: %v", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	awaitGracefulShutdown()
}

func awaitGracefulShutdown() {
	// TODO
}
