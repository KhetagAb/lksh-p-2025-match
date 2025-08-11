package wireset

import (
	"context"
	"github.com/google/wire"
	"match/infra"
	"match/internal/generated/server"
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

	wire.Bind(new(server.ServerInterface), new(*handlers.ServerInterface)),
	transport.CreateServer,

	repositories.NewPlayersRepository,
	wire.Bind(new(players.PlayerRepository), new(*repositories.Players)),
	players.NewPlayerService,

	wire.Bind(new(handlers.RegisterPlayerService), new(*players.PlayerService)),
	handlers.NewRegisterPlayerHandler,
	handlers.NewServerInterface,
)
