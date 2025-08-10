package wireset

import (
	"context"
	"github.com/google/wire"
	"match/infra"
	"match/internal/handlers"
	"match/internal/repositories"
	"match/internal/services/players"
	"match/internal/transport"
)

func NewContextProvider() context.Context {
	return context.Background()
}

var All = wire.NewSet(
	NewContextProvider,
	infra.NewConfig,

	transport.CreateServer,

	repositories.NewPlayersRepository,
	wire.Bind(new(players.PlayerRepository), new(*repositories.Players)),
	players.NewPlayerService,

	wire.Bind(new(handlers.RegisterPlayerService), new(*players.PlayerService)),
	wire.Bind(new(handlers.ValidateRegisterPlayerService), new(*players.PlayerService)),
	handlers.NewRegisterPlayerHandler,
	handlers.NewValidatePlayerHandler,
)
