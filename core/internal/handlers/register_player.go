package handlers

import (
	"context"
	"errors"
	"fmt"
	"github.com/labstack/echo/v4"
	"match/domain"
	"strconv"
)

type (
	RegisterPlayerService interface {
		RegisterUser(ctx context.Context, name string, tgUsername string, tgId int64) (*int64, error)
	}

	RegisterPLayerHandler struct {
		registerPlayerService RegisterPlayerService
	}
)

func (h *RegisterPLayerHandler) RegisterUser(ectx echo.Context) error {
	ctx := context.Background()

	name := ectx.Param("name")
	tgUsername := ectx.Param("tgUsername")
	tgId, err := strconv.ParseInt(ectx.Param("tgId"), 10, 64)
	if err != nil {
		return fmt.Errorf("cannot parse telegram chat id: %v", err)
	}
	//logger.Infof(ctx, "Validating player username: %v", tgUsername)

	playerId, err := h.registerPlayerService.RegisterUser(ctx, name, tgUsername, tgId)
	var playerAlreadyExists *domain.PlayerAlreadyExists
	if errors.As(err, &playerAlreadyExists) {
		//logger.Errorf(ctx, "Player %v ot found", tgUsername)
		return ectx.JSON(409, "User already exists")
	}
	if err != nil {
		//logger.Errorf(ctx, "Internal server error while trying to find %v: %v", tgUsername, err)
		return ectx.JSON(500, err)
	}
	//logger.Infof(ctx, "Player %v has been found succesfully", tgUsername)
	return ectx.JSON(200, struct {
		PlayerId int64 `json:"playerId"`
	}{
		*playerId,
	})
}
