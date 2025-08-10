package players

import (
	"context"
	"match/internal/repositories"
	"match/pkg/errs"
)

type SportSISUser struct {
	TelegramId       int64
	TelegramUsername string
	FullName         string
}

func (c *SportSISUser) AddRecordToDatabase(ctx context.Context) (int64, error) {
	var players repositories.Players
	_, er := players.GetPlayerByTelegramID(ctx, c.TelegramId)

	if er == nil {

		return 0, &errs.UserAlreadyExists{}

	}

	ch, er := players.CreatePlayer(ctx, c.FullName, c.TelegramUsername, c.TelegramId)
	if ch == nil {
		return 0, &errs.DataBaseError{}
	}
	return *ch, er

}

func RegisterUser(ctx context.Context, tgUsername string, tgId int64) (string, int64, error) {
	service := PlayerService{}
	fullName, err := service.ValidateRegisterUser(ctx, tgUsername)
	if err != nil {
		return "", 0, &errs.NoNameError{}
	}
	user := SportSISUser{tgId, tgUsername, fullName}
	coreId, er := user.AddRecordToDatabase(ctx)
	if er != nil {
		return "", 0, er
	}
	return fullName, coreId, nil

}
