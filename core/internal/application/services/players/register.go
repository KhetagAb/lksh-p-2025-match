package players

import (
	"context"
	"errors"
	"fmt"
	domain "match/internal/domain/dao"
	"match/internal/domain/services"
)

type (
	PlayerRepository interface {
		CreatePlayer(ctx context.Context, name, username string, telegramID int64) (*int64, error)
		GetPlayerByTgID(ctx context.Context, telegramID int64) (*domain.Player, error)
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

func (s *PlayerService) RegisterUser(ctx context.Context, name string, tgUsername string, tgId int64) (*int64, bool, error) {
	isRegistered := false
	player, err := s.getPlayer(ctx, tgId)
	if err != nil {
		return nil, false, fmt.Errorf("cannot validate user registration [tgUsername=%v] [tgId=%v]: %w", tgUsername, tgId, err)
	}
	if player != nil {
		return &player.ID, isRegistered, nil
	}

	id, err := s.repository.CreatePlayer(ctx, name, tgUsername, tgId)
	if err != nil {
		return nil, false, fmt.Errorf("cannot create player [name=%v] [tgUsername=%v] [tgId=%v]: %w", name, tgUsername, tgId, err)
	}
	isRegistered = true
	return id, isRegistered, nil
}

func (s *PlayerService) getPlayer(ctx context.Context, tgId int64) (*domain.Player, error) {
	player, err := s.repository.GetPlayerByTgID(ctx, tgId)
	var notFoundError *services.NotFoundError
	if errors.As(err, &notFoundError) {
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("cannot get player by telegram id [tgId=%v]", tgId)
	}

	return player, nil
}
