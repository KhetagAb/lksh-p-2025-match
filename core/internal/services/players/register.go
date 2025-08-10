package players

import (
	"context"
	"fmt"
	"match/internal/repositories"
	"match/pkg/errs"
)

type (
	PlayerRepository interface {
		CreatePlayer(ctx context.Context, name, username string, telegramID int64) (*int64, error)
		// TODO возвращать доменный объект
		GetPlayerByTelegramID(ctx context.Context, telegramID int64) (*repositories.Player, error)
	}

	PlayerService struct {
		repository PlayerRepository
	}
)

func (s *PlayerService) ValidateRegisterUser(ctx context.Context, tgUsername string, tgId int64) (string, error) {
	_, err := s.repository.GetPlayerByTelegramID(ctx, tgId)
	// TODO почистить
	if err == nil {
		return "", &errs.PlayerAlreadyExists{}
	}
	return "", &errs.PlayerNotFound{}
}

func (s *PlayerService) RegisterUser(ctx context.Context, tgUsername string, tgId int64) (string, *int64, error) {
	fullName, err := s.ValidateRegisterUser(ctx, tgUsername, tgId)
	var zero int64 = 0
	if err != nil {
		return "", &zero, fmt.Errorf("cannot validate user registration [tgUsername=%v] [tgId=%v]", tgUsername, tgId)
	}

	id, err := s.repository.CreatePlayer(ctx, fullName, tgUsername, tgId)
	if err != nil {
		return "", &zero, err
	}
	return fullName, id, nil

}
