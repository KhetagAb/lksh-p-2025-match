package wireset

import (
	"context"
	"match/internal/application/handlers"
	"match/internal/application/repositories"
	"match/internal/application/services/activities"
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

	repositories.NewPlayersRepository,
	repositories.NewSportSectionsRepository,
	repositories.NewTeamsRepository,
	repositories.NewActivitiesRepository,

	wire.Bind(new(players.PlayerRepository), new(*repositories.Players)),
	players.NewPlayerService,

	wire.Bind(new(sport.Repository), new(*repositories.SportSections)),
	sport.NewSportSectionService,

	wire.Bind(new(teams.PlayerRepository), new(*repositories.Players)),
	wire.Bind(new(teams.TeamRepository), new(*repositories.Teams)),
	teams.NewTeamService,

	wire.Bind(new(activities.ActivityRepository), new(*repositories.Activities)),
	wire.Bind(new(activities.PlayerRepository), new(*repositories.Players)),
	wire.Bind(new(activities.TeamRepository), new(*repositories.Teams)),
	activities.NewActivityService,

	wire.Bind(new(handlers.RegisterPlayerService), new(*players.PlayerService)),
	handlers.NewRegisterPlayerHandler,
	wire.Bind(new(handlers.GetAllSportSectionService), new(*sport.Service)),
	handlers.NewGetAllSportSectionHandler,
	wire.Bind(new(handlers.GetTeamsByActivityID), new(*teams.TeamService)),
	handlers.NewGetTeamsByActivityIDHandler,
	wire.Bind(new(handlers.GetActivitiesBySportSectionID), new(*activities.ActivityService)),
	handlers.NewGetActivitiesBySportSectionIDHandler,
	wire.Bind(new(handlers.EnrollPlayerInActivity), new(*activities.ActivityService)),
	handlers.NewEnrollPlayerInActivityHandler,
	handlers.NewServerInterface,

	wire.Bind(new(server.ServerInterface), new(*handlers.ServerInterface)),
	transport.CreateServer,
)
