package main

import (
	"context"
	"fmt"
	"match/internal/configs"
	"match/pkg/logger"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	//TODO Logger
	cfg, er := configs.LoadUsers("configs/users.yaml")
	fmt.Println(cfg, er)
	//svc, err := app.InitializeService()
	//if err != nil {
	// panic(fmt.Sprintf("failed to initialize server: %v", err))
	//}
	//cfg := svc.Cfg
	//ctx := svc.Ctx
	//
	//server := svc.HttpServer
	//go func() {
	// if err := server.Start(ctx); err != nil {
	//  logger.Errorf(ctx, "failed to start http server: %v", err)
	// }
	//}()

	//awaitGracefulShutdown(ctx, cfg)
}

func awaitGracefulShutdown(ctx context.Context, cfg *configs.Config) {
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	logger.Info(ctx, "shutting down server...")
	//shutdownCtx, cancel := context.WithTimeout(ctx, cfg.HTTP.ShutdownTimeout)
	//defer cancel()

	//if err := httpServer.Stop(shutdownCtx); err != nil {
	// logger.Fatalf(ctx, "server forced to shutdown: %v", err)
	//}
	logger.Info(ctx, "server exited properly")
}
