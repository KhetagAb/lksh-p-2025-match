package handlers

import (
	"github.com/labstack/echo/v4"
	"net/http"
)

func PingPong(c echo.Context) error {
	return c.String(http.StatusOK, "pong")
}
