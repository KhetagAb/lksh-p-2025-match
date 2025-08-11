package handlers

import (
	"context"
	"errors"
	"github.com/labstack/echo/v4"
	"match/domain"
	"match/internal/generated/server"
	"match/pkg/logger"
)

type (
	RegisterPlayerService interface {
		RegisterUser(ctx context.Context, name string, tgUsername string, tgId int) (*int, bool, error)
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
	var playerAlreadyExists *domain.PlayerAlreadyExists
	if errors.As(err, &playerAlreadyExists) {
		logger.Errorf(ctx, "Player %v ot found", params.TgUsername)
		return ectx.JSON(409, "User already exists")
	}
	if err != nil {
		logger.Errorf(ctx, "Internal server error while trying to find %v: %v", params.TgUsername, err)
		return InternalErrorResponse(ectx, err.Error())
	}

	logger.Infof(ctx, "Player %v has been found succesfully", params.TgUsername)
	httpCode := 200
	if isRegistered {
		httpCode = 201
	}
	return ectx.JSON(httpCode, struct {
		PlayerId int `json:"playerId"`
	}{
		*playerId,
	})
}
