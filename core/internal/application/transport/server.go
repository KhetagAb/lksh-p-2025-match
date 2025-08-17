package transport

import (
	"context"
	"fmt"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"match/internal/generated/server"
	"match/internal/infra"
	"net/http"
)

type HTTPServer struct {
	echo *echo.Echo
	cfg  *infra.Config
}

func CreateServer(
	cfg *infra.Config,
	serverInterface server.ServerInterface,
) *HTTPServer {
	echo := echo.New()

	echo.Use(middleware.Logger())
	echo.Use(middleware.Recover())

	srv := &HTTPServer{
		echo: echo,
		cfg:  cfg,
	}

	server.RegisterHandlers(echo, serverInterface)
	echo.GET("/ping", PingPong)

	return srv
}

func (s *HTTPServer) StartServer() error {
	return s.echo.Start(fmt.Sprintf(":%v", s.cfg.HTTP.Port))
}

func (s *HTTPServer) StopServer(ctx context.Context) error {
	return s.echo.Shutdown(ctx)
}

func (s *HTTPServer) RegisterHealthCheck(healthcheck func(c echo.Context) error) {
	s.echo.GET("/health", healthcheck)
}

func PingPong(c echo.Context) error {
	return c.String(http.StatusOK, "pong")
}
