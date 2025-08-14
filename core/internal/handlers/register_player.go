package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
	"match/internal/generated/server"
	"match/pkg/logger"
	"net/http"
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

func (h *RegisterPlayerHandler) RegisterUser(ectx echo.Context) error {
	ctx := context.Background()
	request := new(server.RegisterPlayerRequest)

	if err := ectx.Bind(request); err != nil {
		logger.Errorf(ctx, "Bad request: register user requires body")
		return ectx.String(http.StatusBadRequest, "Invalid request body")
	}

	logger.Infof(ctx, "Registering player with tg: %v", request.TgUsername)

	playerId, isRegistered, err := h.registerPlayerService.RegisterUser(ctx, request.Name, request.TgUsername, request.TgId)
	if err != nil {
		logger.Errorf(ctx, "Internal server error while trying to find %v: %v", request.TgUsername, err)
		return InternalErrorResponse(ectx, err.Error())
	}

	if isRegistered {
		logger.Infof(ctx, "Player %v registered", request.TgUsername)
		return ectx.JSON(200, server.PlayerRegistrationResponse{Id: *playerId})
	}
	logger.Infof(ctx, "Player %v has been already registered", request.TgUsername)
	return ectx.JSON(201, server.PlayerRegistrationResponse{Id: *playerId})
}
