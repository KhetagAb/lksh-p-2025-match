package wireset

import (
	"match/internal/application/handlers"
	"match/internal/application/repositories"
	"match/internal/application/services/activities"
	"match/internal/application/services/players"
	"match/internal/application/services/sports"
	"match/internal/application/services/teams"
	"match/internal/application/transport"
	"match/internal/generated/server"
	"match/internal/infra"

	"github.com/google/wire"
)

var All = wire.NewSet(
	infra.NewContextProvider,

	infra.NewConfig,
	infra.NewPgxPool,

	// Repositories

	repositories.NewPlayersRepository,
	repositories.NewSportSectionsRepository,
	repositories.NewTeamsRepository,
	repositories.NewActivitiesRepository,

	// Services
	wire.Bind(new(players.PlayerRepository), new(*repositories.Players)),
	players.NewPlayerService,

	wire.Bind(new(sports.SportRepository), new(*repositories.SportSections)),
	sports.NewSportSectionService,

	wire.Bind(new(teams.PlayerRepository), new(*repositories.Players)),
	wire.Bind(new(teams.TeamRepository), new(*repositories.Teams)),
	teams.NewTeamService,

	wire.Bind(new(activities.ActivityRepository), new(*repositories.Activities)),
	wire.Bind(new(activities.PlayerService), new(*repositories.Players)),
	wire.Bind(new(activities.TeamRepository), new(*repositories.Teams)),
	wire.Bind(new(activities.SportRepository), new(*repositories.SportSections)),
	activities.NewActivityService,

	// Handlers

	wire.Bind(new(handlers.RegisterPlayerService), new(*players.PlayerService)),
	handlers.NewRegisterPlayerHandler,

	wire.Bind(new(handlers.GetAllSportSectionService), new(*sports.Service)),
	handlers.NewGetAllSportSectionHandler,

	wire.Bind(new(handlers.GetTeamsByActivityID), new(*teams.TeamService)),
	handlers.NewGetTeamsByActivityIDHandler,

	wire.Bind(new(handlers.GetActivitiesBySportSectionID), new(*activities.ActivityService)),
	handlers.NewGetActivitiesBySportSectionIDHandler,

	wire.Bind(new(handlers.EnrollPlayerInActivity), new(*activities.ActivityService)),
	handlers.NewEnrollPlayerInActivityHandler,

	wire.Bind(new(handlers.CreateActivityService), new(*activities.ActivityService)),
	handlers.NewCreateActivityHandler,

	wire.Bind(new(handlers.DeleteActivityService), new(*activities.ActivityService)),
	handlers.NewDeleteActivityHandler,

	wire.Bind(new(handlers.UpdateActivityService), new(*activities.ActivityService)),
	handlers.NewUpdateActivityHandler,

	wire.Bind(new(handlers.GetPlayerByTgService), new(*players.PlayerService)),
	handlers.NewGetPlayerByTgHandler,

	wire.Bind(new(handlers.DeletePlayerFromActivity), new(*activities.ActivityService)),
	handlers.NewDeletePlayerFromActivityHandler,

	handlers.NewServerInterface,

	// ---

	wire.Bind(new(server.ServerInterface), new(*handlers.ServerInterface)),
	transport.CreateServer,
)
