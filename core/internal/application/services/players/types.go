package players

import (
	"context"
	"match/internal/domain/dao"
)

type (
	PlayerRepository interface {
		CreatePlayer(ctx context.Context, name, username string, telegramID int64) (*int64, error)
		GetPlayerByID(ctx context.Context, telegramID int64) (*dao.Player, error)
		GetPlayerByTgID(ctx context.Context, telegramID int64) (*dao.Player, error)
		GetPlayerByTgUsername(ctx context.Context, telegramUsername string) (*dao.Player, error)
	}

	PlayerService struct {
		repository PlayerRepository
	}
)

func NewPlayerService(
	repository PlayerRepository,
) *PlayerService {
	return &PlayerService{
		repository: repository,
	}
}
