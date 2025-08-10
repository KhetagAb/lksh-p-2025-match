package players

import (
	"context"
	"errors"
	"fmt"
	"match/domain"
)

type (
	PlayerRepository interface {
		CreatePlayer(ctx context.Context, name, username string, telegramID int64) (*int64, error)
		GetPlayerByTelegramID(ctx context.Context, telegramID int64) (*domain.Player, error)
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

func (s *PlayerService) ValidateRegisterUser(ctx context.Context, tgUsername string, tgId int64) error {
	_, err := s.repository.GetPlayerByTelegramID(ctx, tgId)
	var notFoundError *domain.NotFoundError
	if errors.As(err, &notFoundError) {
		return nil
	}
	if err != nil {
		return fmt.Errorf("cannot get player by telegram id [tgId=%v]", tgId)
	}

	return domain.PlayerAlreadyExistsError("Player with tgUsername=%v and tgId=%v already exists", tgUsername, tgId)
}

func (s *PlayerService) RegisterUser(ctx context.Context, name string, tgUsername string, tgId int64) (*int64, error) {
	err := s.ValidateRegisterUser(ctx, tgUsername, tgId)
	if err != nil {
		return nil, fmt.Errorf("cannot validate user registration [tgUsername=%v] [tgId=%v]: %w", tgUsername, tgId, err)
	}

	id, err := s.repository.CreatePlayer(ctx, name, tgUsername, tgId)
	if err != nil {
		return nil, fmt.Errorf("cannot create player [name=%v] [tgUsername=%v] [tgId=%v]: %w", name, tgUsername, tgId, err)
	}
	return id, nil

}
