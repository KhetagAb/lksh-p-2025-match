package repositories

import (
	"context"

	"match/internal/domain"
	"github.com/jackc/pgx/v5/pgxpool"
)

type Players struct {
	pool *pgxpool.Pool
}

func (p *Players) CreatePlayer(ctx context.Context, name, username string, telegramID int64) (*int64, error) {
	query := `
        INSERT INTO players (name, username, telegram_id)
        VALUES ($1, $2, $3)
        RETURNING id
    `

	var id int64
	err := p.pool.QueryRow(ctx, query, name, username, telegramID).Scan(&id)
	if err != nil {
		return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}

	return &id, nil
}

func (p *Players) GetPlayerByID(ctx context.Context, id int64) (*Player, error) {
	query := `
		SELECT * FROM players
		WHERE id = $1
	`

	var telegramID int64
	var name string
	var username string

	err := p.pool.QueryRow(ctx, query, id).Scan(&id, &name, &username, &telegramID)
	if err != nil {
		return nil, &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return &Player{id, name, username, telegramID}, nil
}

func (p *Players) GetPlayerByTelegramID(ctx context.Context, telegramID int64) (*Player, error) {
	query := `
		SELECT * FROM players
		WHERE telegram_id = $1
	`

	var id int64
	var name string
	var username string

	err := p.pool.QueryRow(ctx, query, telegramID).Scan(&id, &name, &username, &telegramID)
	if err != nil {
		return nil, &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return &Player{id, name, username, telegramID}, nil
}

func (p *Players) DeletePlayerByID(ctx context.Context, id int64) error {
	query := `
		DELETE FROM players
		WHERE id = $1
	`

	_, err := p.pool.Exec(ctx, query, id)
	if err != nil {
		return &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}

	return nil
}
