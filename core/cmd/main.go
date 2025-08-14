package main

import (
	"fmt"
	g "match/internal/generated/"
	"match/internal/infra"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	infra.Init()
	svc, err := g.app.InitializeApp()
	if err != nil {
		panic(fmt.Sprintf("failed to initialize server: %v", err))
	}

	server := g.svc.HttpServer
	go func() {
		if err := server.StartServer(); err != nil {
			infra.Errorf(svc.Ctx, "failed to start http server: %v", err)
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
