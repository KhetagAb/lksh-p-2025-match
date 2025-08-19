package players

import (
	"context"
	"fmt"
)

func (s *PlayerService) RegisterUser(ctx context.Context, name string, tgUsername string, tgId int64) (id *int64, isRegistered bool, err error) {
	player, err := s.GetPlayerByTgID(ctx, tgId)
	if err != nil {
		return nil, false, fmt.Errorf("cannot validate user registration [tgUsername=%v] [tgId=%v]: %w", tgUsername, tgId, err)
	}
	if player != nil {
		return &player.ID, false, nil
	}

	id, err = s.repository.CreatePlayer(ctx, name, tgUsername, tgId)
	if err != nil {
		return nil, false, fmt.Errorf("cannot create player [name=%v] [tgUsername=%v] [tgId=%v]: %w", name, tgUsername, tgId, err)
	}
	return id, true, nil
}
