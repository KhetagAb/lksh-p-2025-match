package transport

import (
	"fmt"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"match/infra"
	"match/internal/handlers"
	"net/http"
)

type HTTPServer struct {
	echo *echo.Echo
	cfg  *infra.Config

	validatePlayerHandler *handlers.ValidatePlayerHandler
}

func (s *HTTPServer) RegisterEndpoints() {
	s.echo.GET("/ping", PingPong)
	s.echo.GET("/validate_register_user", s.validatePlayerHandler.ValidateRegisterUser)
}

func CreateServer(
	cfg *infra.Config,
	validatePlayerHandler *handlers.ValidatePlayerHandler,
) *HTTPServer {
	server := echo.New()

	server.Use(middleware.Logger())
	server.Use(middleware.Recover())

	srv := &HTTPServer{
		echo: server,
		cfg:  cfg,

		validatePlayerHandler: validatePlayerHandler,
	}
	srv.RegisterEndpoints()

	return srv
}

func (s *HTTPServer) StartServer() error {
	return s.echo.Start(fmt.Sprintf(":%v", s.cfg.HTTP.Port))
}

func PingPong(c echo.Context) error {
	return c.String(http.StatusOK, "pong")
}
