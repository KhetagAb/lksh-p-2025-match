package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
	"match/domain"
	"strconv"
)

type (
	ValidatePlayerService interface {
		ValidateRegisterUser(ctx context.Context, tgUsername string, tgId int64) error
	}

	ValidatePlayerHandler struct {
		validatePlayerService ValidatePlayerService
	}
)

func (h *ValidatePlayerHandler) ValidateRegisterUser(ectx echo.Context) error {
	ctx := context.Background()
	tgUsername := ectx.Param("tgUsername")
	tgId, _ := strconv.ParseInt("tgId", 10, 64)
	//logger.Infof(ctx, "Validating player username: %v", tgUsername)

	err := h.validatePlayerService.ValidateRegisterUser(ctx, tgUsername, tgId)
	if err != nil {
		if _, ok := err.(*domain.NotFoundError); ok {
			//logger.Errorf(ctx, "Player %v ot found", tgUsername)
			return ectx.JSON(404, "User not found")
		}
		//logger.Errorf(ctx, "Internal server error while trying to find %v: %v", tgUsername, err)
		return ectx.JSON(500, err)
	}
	//logger.Infof(ctx, "Player %v has been found succesfully", tgUsername)
	return ectx.JSON(200, nil)
}
