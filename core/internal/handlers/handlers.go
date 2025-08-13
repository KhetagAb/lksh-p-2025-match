package handlers

import (
	"match/internal/generated/server"

	"github.com/labstack/echo/v4"
)

type ServerInterface struct {
	registerPlayer                  *RegisterPlayerHandler
	createTournament                *CreateTournamentHandler
	getCoreActivityByID             *GetCoreActivityByIDHandler
	getCoreActivityBySportSectionID *GetCoreActivityBySportSectionIDHandler
	postCoreActivityIDEnroll        *PostCoreActivityIDEnrollHandler
}

func (s ServerInterface) GetCoreActivityById(ctx echo.Context, id int64) error {
	return s.getCoreActivityByID.GetCoreActivityByID(ctx, id)
}

func (s ServerInterface) GetCoreActivityBySportSectionId(ctx echo.Context, id int64) error {
	return s.getCoreActivityBySportSectionID.GetCoreActivityBySportSectionID(ctx, id)
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

func NewServerInterface(registerPlayer *RegisterPlayerHandler, createTournament *CreateTournamentHandler, getCoreActivityBySportSectionID *GetCoreActivityBySportSectionIDHandler) *ServerInterface {
	return &ServerInterface{
		registerPlayer:                  registerPlayer,
		createTournament:                createTournament,
		getCoreActivityBySportSectionID: getCoreActivityBySportSectionID,
	}
}
