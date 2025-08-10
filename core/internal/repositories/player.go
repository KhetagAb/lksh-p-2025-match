package repositories

import (
	"context"
	_ "embed"

	"match/internal/domain"

	"github.com/jackc/pgx/v5/pgxpool"
)

var (
	//go:embed queries/player/create.sql
	createPlayerQuery string

	//go:embed queries/player/get-by-id.sql
	getByIDPlayerQuery string

	//go:embed queries/player/get-by-telegram-id.sql
	getByTelegramIDPlayerQuery string

	//go:embed queries/player/delete.sql
	deletePlayerQuery string
)

type Players struct {
	pool *pgxpool.Pool
}

func (p *Players) CreatePlayer(ctx context.Context, name, username string, telegramID int64) (*int64, error) {
	var id int64
	err := p.pool.QueryRow(ctx, createPlayerQuery, name, username, telegramID).Scan(&id)
	if err != nil {
		return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}

	return &id, nil
}

func (p *Players) GetPlayerByID(ctx context.Context, id int64) (*Player, error) {
	var telegramID int64
	var name string
	var username string

	err := p.pool.QueryRow(ctx, getByIDPlayerQuery, id).Scan(&id, &name, &username, &telegramID)
	if err != nil {
		return nil, &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return &Player{id, name, username, telegramID}, nil
}

func (p *Players) GetPlayerByTelegramID(ctx context.Context, telegramID int64) (*Player, error) {
	var id int64
	var name string
	var username string

	err := p.pool.QueryRow(ctx, getByTelegramIDPlayerQuery, telegramID).Scan(&id, &name, &username, &telegramID)
	if err != nil {
		return nil, &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return &Player{id, name, username, telegramID}, nil
}

func (p *Players) DeletePlayerByID(ctx context.Context, id int64) error {
	commandTag, err := p.pool.Exec(ctx, deletePlayerQuery, id)
	if err != nil {
		return &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}
	if commandTag.RowsAffected() != 1 {
		return &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return nil
}
