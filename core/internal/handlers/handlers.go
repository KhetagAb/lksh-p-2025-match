package handlers

import (
	"github.com/labstack/echo/v4"
	"match/internal/generated/server"
)

type ServerInterface struct {
	registerPlayer *RegisterPlayerHandler
}

func (s *ServerInterface) RegisterPlayer(ctx echo.Context, params server.RegisterPlayerParams) error {
	return s.registerPlayer.RegisterUser(ctx, params)
}

var _ server.ServerInterface = &ServerInterface{}

func NewServerInterface(registerPlayer *RegisterPlayerHandler) *ServerInterface {
	return &ServerInterface{
		registerPlayer: registerPlayer,
	}
}
