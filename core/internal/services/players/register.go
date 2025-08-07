package players

import (
	"context"
	"match/pkg/errs"
)

type TgUsernameToName interface {
	GetTgUsernameToName() map[string]string
}

type PlayerService struct {
	tgUsernameToName TgUsernameToName
}

func (s *PlayerService) ValidateRegisterUser(ctx context.Context, tgUsername string) (string, error) {
	tgUserNameToName := s.tgUsernameToName.GetTgUsernameToName()
	val, ok := tgUserNameToName[tgUsername]
	if ok {
		return val, nil
	}
	return "", &errs.PlayerNotFound{}
}
