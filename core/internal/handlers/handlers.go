package handlers

import (
	"github.com/labstack/echo/v4"
	"match/internal/generated/server"
)

type ServerInterface struct {
	registerPlayer   *RegisterPlayerHandler
	createTournament *CreateTournamentHandler
}

func (s *ServerInterface) CreateTournament(ctx echo.Context, params server.CreateTournamentParams) error {
	return s.createTournament.CreateTournament(ctx, params)
}

func (s *ServerInterface) GetCoreSportGetSport(ctx echo.Context, sport string) error {
	//TODO implement me
	panic("implement me")
}

func (s *ServerInterface) GetCoreSportsGet(ctx echo.Context) error {
	//TODO implement me
	panic("implement me")
}

func (s *ServerInterface) GetCoreSportsGetAll(ctx echo.Context) error {
	//TODO implement me
	panic("implement me")
}

//func (s *ServerInterface) CreateTournament(ctx echo.Context, params server.CreateTournamentParams) error {
//	//TODO implement me
//	panic("implement me")
//}

func (s *ServerInterface) RegisterPlayer(ctx echo.Context, params server.RegisterPlayerParams) error {
	return s.registerPlayer.RegisterUser(ctx, params)
}

var _ server.ServerInterface = &ServerInterface{}

func NewServerInterface(registerPlayer *RegisterPlayerHandler, createTournament *CreateTournamentHandler) *ServerInterface {
	return &ServerInterface{
		registerPlayer:   registerPlayer,
		createTournament: createTournament,
	}
}
