package infra

import (
	"context"
	"errors"

	"github.com/jackc/pgx/v5"
)

type Transaction struct{ pgx.Tx }

func GetConnection() (*pgx.Conn, error) {
	ctx := context.Background()
	conn, err := pgx.Connect(ctx, DBURL(&GetConfig().Database)) // TODO: add di
	if err != nil {
		return conn, errors.New("postgres connection error")
	}
	defer conn.Close(ctx)
	return conn, nil
}

func OpenTransaction(s *Transaction) (context.Context, pgx.Tx, error) {
	ctx := context.Background()
	transaction, err := s.Begin(ctx)
	if err != nil {
		return ctx, transaction, errors.New("")
	}
	return ctx, transaction, nil
}

func CloseTransaction(s *Transaction, ctx context.Context) error {
	err := s.Commit(ctx)
	if err != nil {
		return err
	}
	defer s.Rollback(ctx)
	return nil
}
