package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
	"match/pkg/errs"
	"strconv"
)

type (
	RegisterPlayerService interface {
		RegisterUser(ctx context.Context, tgUsername string, tgId int64) (string, int64, error)
	}

	RegisterPLayerHandler struct {
		registerPlayerService RegisterPlayerService
	}
)

func (h *RegisterPLayerHandler) RegisterUser(ectx echo.Context) error {
	ctx := context.Background()
	tgUsername := ectx.Param("tgUsername")
	tgId, _ := strconv.ParseInt(ectx.Param("tgId"), 10, 64)
	//logger.Infof(ctx, "Validating player username: %v", tgUsername)

	playerName, playerId, err := h.registerPlayerService.RegisterUser(ctx, tgUsername, tgId)

	if err != nil {
		if _, ok := err.(*errs.UserAlreadyExists); ok {
			//logger.Errorf(ctx, "Player %v ot found", tgUsername)
			return ectx.JSON(409, "User alredy exists")
		}
		//logger.Errorf(ctx, "Internal server error while trying to find %v: %v", tgUsername, err)
		return ectx.JSON(500, err)
	}
	//logger.Infof(ctx, "Player %v has been found succesfully", tgUsername)
	return ectx.JSON(200, struct {
		PlayerName string `json:"playerName"`
		PlayerId   int64  `json:"playerId"`
	}{
		playerName, playerId,
	})
}
