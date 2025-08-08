package infra

import (
	"context"
	"errors"

	"github.com/jackc/pgx/v5"
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
	err = s.Rollback(ctx)
	if err != nil {
		return err
	}
	return nil
}
