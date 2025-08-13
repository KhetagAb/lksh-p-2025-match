package handlers

import (
	"github.com/labstack/echo/v4"
	"match/internal/generated/server"
)

type ServerInterface struct {
	registerPlayer   *RegisterPlayerHandler
	createTournament *CreateTournamentHandler
}

func (s ServerInterface) GetCoreActivityById(ctx echo.Context, id int64) error {
	//TODO implement me
	panic("implement me")
}

func (s ServerInterface) GetCoreActivityBySportSectionId(ctx echo.Context, id int64) error {
	//TODO implement me
	panic("implement me")
}

func (s ServerInterface) PostCoreActivityIdEnroll(ctx echo.Context, id string) error {
	//TODO implement me
	panic("implement me")
}

func (s ServerInterface) RegisterPlayer(ctx echo.Context) error {
	//TODO implement me
	panic("implement me")
}

func (s ServerInterface) GetCoreSportList(ctx echo.Context) error {
	//TODO implement me
	panic("implement me")
}

var _ server.ServerInterface = &ServerInterface{}

func NewServerInterface(registerPlayer *RegisterPlayerHandler, createTournament *CreateTournamentHandler) *ServerInterface {
	return &ServerInterface{
		registerPlayer:   registerPlayer,
		createTournament: createTournament,
	}
}
