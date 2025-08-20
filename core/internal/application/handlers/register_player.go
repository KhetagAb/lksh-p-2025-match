package handlers

import (
	"context"
	"fmt"
	"match/internal/generated/server"
	"match/internal/infra"

	"github.com/labstack/echo/v4"
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

func validateRegisterPlayerRequest(request *server.RegisterPlayerRequest) error {
	if len(request.Name) == 0 {
		return fmt.Errorf("name field is required and cannot be empty")
	}

	if len(request.TgUsername) == 0 {
		return fmt.Errorf("tgUsername field is required and cannot be empty")
	}

	if request.TgId == 0 {
		return fmt.Errorf("tgId field is required and cannot be zero")
	}

	return nil
}

func (h *RegisterPlayerHandler) RegisterUser(ectx echo.Context) error {
	ctx := context.Background()
	request := new(server.RegisterPlayerRequest)

	if err := ectx.Bind(request); err != nil {
		infra.Errorf(ctx, "Bad request: register user requires body")
		return BadRequestErrorResponsef(ectx, "Invalid request body: %v", err)
	}

	if err := validateRegisterPlayerRequest(request); err != nil {
		infra.Errorf(ctx, "Validation error: %v", err)
		return BadRequestErrorResponsef(ectx, err.Error())
	}

	infra.Infof(ctx, "Registering player with tg: %v", request.TgUsername)
	playerId, isRegistered, err := h.registerPlayerService.RegisterUser(ctx, request.Name, request.TgUsername, request.TgId)
	if err != nil {
		infra.Errorf(ctx, "Internal server error while trying to find %v: %v", request.TgUsername, err)
		return InternalErrorResponsef(ectx, err.Error())
	}
	if isRegistered {
		infra.Infof(ctx, "Player %v registered", request.TgUsername)
		return ectx.JSON(201, server.PlayerRegistrationResponse{Id: *playerId})
	}
	infra.Infof(ctx, "Player %v has been already registered", request.TgUsername)
	return ectx.JSON(200, server.PlayerRegistrationResponse{Id: *playerId})
}
