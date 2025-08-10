package infra

import (
	"context"
	"errors"

	"github.com/jackc/pgx/v5"
	"go.uber.org/fx"
)

type Transaction struct{ pgx.Tx }

func GetConnection() (context.Context, *pgx.Conn, error) {
	ctx := context.Background()
	connection, err := pgx.Connect(ctx, DBURL(&GetConfig().Database)) // TODO: add di
	if err != nil {
		return ctx, connection, errors.New("postgres connection error")
	}
	return ctx, connection, nil
}

func CloseConnection(ctx context.Context, connection pgx.Conn) error {
	err := connection.Close(ctx)
	if err != nil {
		return err
	}
	return nil
}

func WithTransaction(s *Transaction, ctx context.Context, lc fx.Lifecycle) (context.Context, pgx.Tx, error) {
	transaction, err := s.Begin(ctx)
	if err != nil {
		return ctx, transaction, errors.New("")
	}
	lc.Append(fx.Hook{
		OnStop: func(context.Context) error {
			if err := s.Commit(ctx); err != nil {
				return err
			}
			if err = s.Rollback(ctx); err != nil {
				return err
			}
			return nil
		},
	})
	return ctx, transaction, nil
}
