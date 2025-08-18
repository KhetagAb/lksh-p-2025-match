package players

import (
	"context"
	"errors"
	"fmt"
	"match/internal/domain/dao"
	"match/internal/domain/services"
)

func (s *PlayerService) getPlayerById(ctx context.Context, tgId int64) (*dao.Player, error) {
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

func (s *PlayerService) getPlayerByUsername(ctx context.Context, tgUsername string) (*dao.Player, error) {
	player, err := s.repository.GetPlayerByTgUsername(ctx, tgUsername)
	var notFoundError *services.NotFoundError
	if errors.As(err, &notFoundError) {
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("cannot get player by telegram username [tgUsername=%v]", tgUsername)
	}

	return player, nil
}
