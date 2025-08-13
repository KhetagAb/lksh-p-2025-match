package wireset

import (
	"context"
	"github.com/google/wire"
	"match/infra"
	"match/internal/generated/server"
	"match/internal/handlers"
	"match/internal/repositories"
	"match/internal/services/players"
	"match/internal/services/tournaments"
	"match/internal/transport"
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

	repositories.NewTournamentsRepository,
	wire.Bind(new(tournaments.TournamentRepository), new(*repositories.Tournaments)),
	tournaments.NewTournamentService,

	wire.Bind(new(handlers.RegisterPlayerService), new(*players.PlayerService)),
	wire.Bind(new(handlers.CreateTournamentService), new(*tournaments.TournamentService)),
	handlers.NewRegisterPlayerHandler,
	handlers.NewServerInterface,
	handlers.NewCreateTournamentHandler,
)
