package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
	"match/internal/generated/server"
	"match/pkg/logger"
)

type (
	RegisterPlayerService interface {
		RegisterUser(ctx context.Context, name string, tgUsername string, tgId int64) (*int64, bool, error)
	}

	RegisterPlayerHandler struct {
		registerPlayerService RegisterPlayerService
	}
)

func NewRegisterPlayerHandler(
	registerPlayerService RegisterPlayerService,
) *RegisterPlayerHandler {
	return &RegisterPlayerHandler{
		registerPlayerService: registerPlayerService,
	}
}

func (h *RegisterPlayerHandler) RegisterUser(ectx echo.Context, params server.RegisterPlayerParams) error {
	ctx := context.Background()

	logger.Infof(ctx, "Validating player username: %v", params.TgUsername)

	playerId, isRegistered, err := h.registerPlayerService.RegisterUser(ctx, params.Name, params.TgUsername, params.TgId)
	if err != nil {
		logger.Errorf(ctx, "Internal server error while trying to find %v: %v", params.TgUsername, err)
		return InternalErrorResponse(ectx, err.Error())
	}

	logger.Infof(ctx, "Player %v has been found succesfully", params.TgUsername)
	httpCode := 201
	if isRegistered {
		httpCode = 200
	}
	return ectx.JSON(httpCode, server.PlayerRegistrationResponse{Id: playerId})
}
