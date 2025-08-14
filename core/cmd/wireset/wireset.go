package wireset

import (
	"context"
	"match/internal/application/handlers"
	"match/internal/application/repositories"
	"match/internal/application/services/players"
	"match/internal/application/services/sport"
	"match/internal/application/services/teams"
	"match/internal/application/transport"
	"match/internal/generated/server"
	"match/internal/infra"

	"github.com/google/wire"
)

func NewContextProvider() context.Context {
	return context.Background()
}

var All = wire.NewSet(
	NewContextProvider,

	infra.NewConfig,
	infra.NewPgxPool,

	wire.Bind(new(server.ServerInterface), new(*handlers.ServerInterface)),
	transport.CreateServer,

	repositories.NewPlayersRepository,
	wire.Bind(new(players.PlayerRepository), new(*repositories.Players)),
	players.NewPlayerService,

	repositories.NewSportSectionsRepository,
	wire.Bind(new(sport.Repository), new(*repositories.SportSections)),
	sport.NewSportSectionService,

	repositories.NewTeamsRepository,
	wire.Bind(new(teams.TeamRepository), new(*repositories.Teams)),
	teams.NewTeamService,

	wire.Bind(new(handlers.RegisterPlayerService), new(*players.PlayerService)),
	handlers.NewRegisterPlayerHandler,
	wire.Bind(new(handlers.GetAllSportSectionService), new(*sport.Service)),
	handlers.NewGetAllSportSectionHandler,
	wire.Bind(new(handlers.GetTeamsByActivityID), new(*teams.TeamService)),
	handlers.NewGetTeamsByActivityIDHandler,
	handlers.NewGetActivitiesBySportSectionIDHandler,
	handlers.NewEnrollPlayerInActivityHandler,
	handlers.NewServerInterface,
)
