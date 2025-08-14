package wireset

import (
	"context"
	"github.com/google/wire"
	"match/internal/application/handlers"
	"match/internal/application/repositories"
	"match/internal/application/services/players"
	"match/internal/application/services/sport"
	"match/internal/application/services/tournaments"
	"match/internal/application/transport"
	"match/internal/generated/presentation"
	"match/internal/infra"
)

func NewContextProvider() context.Context {
	return context.Background()
}

var All = wire.NewSet(
	NewContextProvider,

	infra.NewConfig,
	infra.NewPgxPool,

	wire.Bind(new(presentation.ServerInterface), new(*handlers.ServerInterface)),
	transport.CreateServer,

	repositories.NewPlayersRepository,
	wire.Bind(new(players.PlayerRepository), new(*repositories.Players)),
	players.NewPlayerService,

	repositories.NewTournamentsRepository,
	wire.Bind(new(tournaments.TournamentRepository), new(*repositories.Tournaments)),
	tournaments.NewTournamentService,

	repositories.NewSportSectionsRepository,
	wire.Bind(new(sport.Repository), new(*repositories.SportSections)),
	sport.NewSportSectionService,

	wire.Bind(new(handlers.RegisterPlayerService), new(*players.PlayerService)),
	handlers.NewRegisterPlayerHandler,
	wire.Bind(new(handlers.GetAllSportSectionService), new(*sport.Service)),
	handlers.NewGetAllSportSectionHandler,
	handlers.NewServerInterface,
)
