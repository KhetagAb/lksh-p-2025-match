//go:build wireinject
// +build wireinject

package wireset

import (
	"context"
	"github.com/google/wire"
	"match/internal/application/transport"
	"match/internal/infra"
)

type App struct {
	Ctx        context.Context
	Cfg        *infra.Config
	HttpServer *transport.HTTPServer
}

func InitializeApp() (*App, error) {
	wire.Build(
		All,
		wire.Struct(new(App), "*"),
	)
	return nil, nil
}
