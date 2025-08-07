package transport

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"

	"match/internal/handlers"
)

func RegisterEndpoints(server *echo.Echo) {
	server.GET("/ping", handlers.PingPong)
	// registering endpoints here
	// TODO прокинуть сервис игрока
	server.GET("/", handlers.Handler{}.ValidateRegisterUser)

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
}
