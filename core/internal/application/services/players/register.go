package players

import (
	"context"
	"fmt"
)

func (s *PlayerService) RegisterUser(ctx context.Context, name string, tgUsername string, tgId int64) (*int64, bool, error) {
	isRegistered := false
	player, err := s.getPlayerById(ctx, tgId)
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
