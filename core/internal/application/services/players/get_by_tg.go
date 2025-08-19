package players

import (
	"context"
	"errors"
	"fmt"
	"match/internal/domain/dao"
	"match/internal/domain/services"
)

func (s *PlayerService) GetPlayerByID(ctx context.Context, tgId int64) (*dao.Player, error) {
	player, err := s.repository.GetPlayerByID(ctx, tgId)
	var notFoundError *services.NotFoundError
	if errors.As(err, &notFoundError) {
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("cannot get player by core id=%v", tgId)
	}

	return player, nil
}

func (s *PlayerService) GetPlayerByTgID(ctx context.Context, tgId int64) (*dao.Player, error) {
	player, err := s.repository.GetPlayerByTgID(ctx, tgId)
	var notFoundError *services.NotFoundError
	if errors.As(err, &notFoundError) {
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("cannot get player by telegram id=%v", tgId)
	}

	return player, nil
}

func (s *PlayerService) GetPlayerByTgUsername(ctx context.Context, tgUsername string) (*dao.Player, error) {
	player, err := s.repository.GetPlayerByTgUsername(ctx, tgUsername)
	var notFoundError *services.NotFoundError
	if errors.As(err, &notFoundError) {
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("cannot get player by telegram username=%v", tgUsername)
	}

	return player, nil
}
