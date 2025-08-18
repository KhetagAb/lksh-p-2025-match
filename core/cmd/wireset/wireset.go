package wireset

import (
	"match/internal/application/handlers"
	activities2 "match/internal/application/handlers/activities"
	players2 "match/internal/application/handlers/players"
	"match/internal/application/handlers/sports"
	teams2 "match/internal/application/handlers/teams"
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

var All = wire.NewSet(
	infra.NewContextProvider,

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

	wire.Bind(new(players2.RegisterPlayerService), new(*players.PlayerService)),
	players2.NewRegisterPlayerHandler,
	wire.Bind(new(sports.GetAllSportSectionService), new(*sport.Service)),
	sports.NewGetAllSportSectionHandler,
	wire.Bind(new(teams2.GetTeamsByActivityID), new(*teams.TeamService)),
	teams2.NewGetTeamsByActivityIDHandler,
	wire.Bind(new(activities2.GetActivitiesBySportSectionID), new(*activities.ActivityService)),
	activities2.NewGetActivitiesBySportSectionIDHandler,
	wire.Bind(new(activities2.EnrollPlayerInActivity), new(*activities.ActivityService)),
	activities2.NewEnrollPlayerInActivityHandler,
	handlers.NewServerInterface,

	wire.Bind(new(server.ServerInterface), new(*handlers.ServerInterface)),
	transport.CreateServer,
)
