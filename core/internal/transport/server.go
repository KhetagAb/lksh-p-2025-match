package transport

import (
	"errors"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"log/slog"
	"match/internal/handlers"
	"net/http"
)

func RegisterEndpoints(server *echo.Echo) {
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

func StartServer(server *echo.Echo) {
	// **IMPORTANT:** replace with config later
	err := server.Start(":8080")

	if err != nil && !errors.Is(err, http.ErrServerClosed) {
		slog.Error("failed to start server", "error", err)
	}
}
