package transport

import (
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

	return srv
}

func (s *HTTPServer) StartServer() error {
	return s.echo.Start(fmt.Sprintf(":%v", s.cfg.HTTP.Port))
}

func PingPong(c echo.Context) error {
	return c.String(http.StatusOK, "pong")
}
