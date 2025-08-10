//go:build wireinject
// +build wireinject

package app

import (
	"context"
	"github.com/google/wire"
	"match/cmd/wireset"
	"match/infra"
	"match/internal/transport"
)

type App struct {
	Ctx        context.Context
	Cfg        *infra.Config
	HttpServer *transport.HTTPServer
}

func InitializeApp() (*App, error) {
	wire.Build(
		wireset.All,
		wire.Struct(new(App), "*"),
	)
	return nil, nil
}
