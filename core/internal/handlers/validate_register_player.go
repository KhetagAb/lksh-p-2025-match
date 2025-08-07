package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
	"match/pkg/errs"
)

type (
	ValidatePlayerService interface {
		ValidateRegisterUser(ctx context.Context, tgUsername string) (string, error)
	}

	ValidatePLayerHandler struct {
		validatePlayerService ValidatePlayerService
	}
)

func (h *ValidatePLayerHandler) ValidateRegisterUser(ectx echo.Context) error {
	ctx := context.Background()
	tgUsername := ectx.Param("tgUsername")

	//logger.Infof(ctx, "Validating player username: %v", tgUsername)


	playerName, err := h.validatePlayerService.ValidateRegisterUser(ctx, tgUsername)

	if err != nil {
		if _, ok := err.(*errs.PlayerNotFound); ok {
			//logger.Errorf(ctx, "Player %v ot found", tgUsername)
			return ectx.JSON(404, "User not found")
		}
		//logger.Errorf(ctx, "Internal server error while trying to find %v: %v", tgUsername, err)
		return ectx.JSON(500, err)
	}
	//logger.Infof(ctx, "Player %v has been found succesfully", tgUsername)
	return ectx.JSON(200, playerName)
}
