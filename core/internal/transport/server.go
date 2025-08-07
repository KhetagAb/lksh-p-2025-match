package transport

import (
	"fmt"
	"log/slog"
	"os"
	"os/signal"
	"syscall"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func RegisterEndpoints(server *echo.Echo) {
	// registering endpoints here
}

func GetServer() *echo.Echo {
	server := echo.New()

	server.Use(middleware.Logger())
	server.Use(middleware.Recover())

	RegisterEndpoints(server)
	return server
}

func RunServer(server *echo.Echo) {
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		// TODO: replace port with config later
		if err := server.Start(":8080"); err != nil {
			panic(fmt.Sprintf("failed to initialize server: %v", err))
		}
	}()
	<-quit
	slog.Info("shutting down server...")
}
