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
	query, err := GetQuery("player", "create")
	if err != nil {
		return nil, &domain.FailedLoadingResourcesError{Code: domain.FailedLoadingResources, Message: err.Error()}
	}

	var id int64
	err = p.pool.QueryRow(ctx, *query, name, username, telegramID).Scan(&id)
	if err != nil {
		return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}

	return &id, nil
}

func (p *Players) GetPlayerByID(ctx context.Context, id int64) (*Player, error) {
	query, err := GetQuery("player", "get-by-id")
	if err != nil {
		return nil, &domain.FailedLoadingResourcesError{Code: domain.FailedLoadingResources, Message: err.Error()}
	}

	var telegramID int64
	var name string
	var username string

	err = p.pool.QueryRow(ctx, *query, id).Scan(&id, &name, &username, &telegramID)
	if err != nil {
		return nil, &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return &Player{id, name, username, telegramID}, nil
}

func (p *Players) GetPlayerByTelegramID(ctx context.Context, telegramID int64) (*Player, error) {
	query, err := GetQuery("player", "get-by-telegram-id")
	if err != nil {
		return nil, &domain.FailedLoadingResourcesError{Code: domain.FailedLoadingResources, Message: err.Error()}
	}

	var id int64
	var name string
	var username string

	err = p.pool.QueryRow(ctx, *query, telegramID).Scan(&id, &name, &username, &telegramID)
	if err != nil {
		return nil, &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return &Player{id, name, username, telegramID}, nil
}

func (p *Players) DeletePlayerByID(ctx context.Context, id int64) error {
	query, err := GetQuery("player", "delete")
	if err != nil {
		return &domain.FailedLoadingResourcesError{Code: domain.FailedLoadingResources, Message: err.Error()}
	}

	_, err = p.pool.Exec(ctx, *query, id)
	if err != nil {
		return &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}

	return nil
}
