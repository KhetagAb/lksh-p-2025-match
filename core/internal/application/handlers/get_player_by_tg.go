package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
	"match/internal/domain/dao"
	"match/internal/generated/server"
	"match/internal/infra"
	"net/http"
)

type (
	GetPlayerByIdService interface {
		GetPlayerByTgID(ctx context.Context, telegramID int64) (*dao.Player, error)
		GetPlayerByTgUsername(ctx context.Context, telegramUsername int64) (*dao.Player, error)
	}

	GetPlayerByIdHandler struct {
		getPlayerByIdService GetPlayerByIdService
	}
)

func NewGetPlayerByIdHandler(
	getPlayerByIdService GetPlayerByIdService,
) *GetPlayerByIdHandler {
	return &GetPlayerByIdHandler{
		getPlayerByIdService: getPlayerByIdService,
	}
}

func (h *GetPlayerByIdHandler) GetPlayerByTg(ectx echo.Context) error {
	ctx := context.Background()
	request := new(server.GetCorePlayerByTgParams)

	if err := ectx.Bind(request); err != nil {
		infra.Errorf(ctx, "Bad request: register user requires body")
		return ectx.String(http.StatusBadRequest, "Invalid request body")
	}

	if request.TgUsername == nil && request.TgId != nil {
		infra.Infof(ctx, "Getting player with tg_id=%d", request.TgId)
		player, err := h.getPlayerByIdService.GetPlayerByTgID(ctx, *request.TgId)
		if err != nil {
			infra.Errorf(ctx, "Internal server error while trying to get player by tgId %v: %v", request.TgId, err)
			return InternalErrorResponse(ectx, err.Error())
		}
		return ectx.JSON(200, server.GetCorePlayerByTgParams{TgId: &player.TgID, TgUsername: &player.TgUsername})
	} else if request.TgUsername != nil && request.TgId == nil {
		infra.Infof(ctx, "Getting player with tg_username=%s", request.TgUsername)
		player, err := h.getPlayerByIdService.GetPlayerByTgUsername(ctx, *request.TgId)
		if err != nil {
			infra.Errorf(ctx, "Internal server error while trying to get player by tg_username %v: %v", request.TgUsername, err)
			return InternalErrorResponse(ectx, err.Error())
		}
		return ectx.JSON(200, server.GetCorePlayerByTgParams{TgId: &player.TgID, TgUsername: &player.TgUsername})
	} else if request.TgUsername != nil && request.TgId != nil {
		infra.Infof(ctx, "Getting player with tg_id=%d and tg_username=%s", request.TgId, request.TgUsername)
		playerById, err := h.getPlayerByIdService.GetPlayerByTgID(ctx, *request.TgId)
		if err != nil {
			infra.Errorf(ctx, "Internal server error while trying to get player by tgId %v: %v", request.TgId, err)
			return InternalErrorResponse(ectx, err.Error())
		}
		playerByUsername, err := h.getPlayerByIdService.GetPlayerByTgID(ctx, *request.TgId)
		if err != nil {
			infra.Errorf(ctx, "Internal server error while trying to get player by tg_username %v: %v", request.TgUsername, err)
			return InternalErrorResponse(ectx, err.Error())
		}
		if playerById.ID == playerByUsername.ID {
			return ectx.JSON(200, server.GetCorePlayerByTgParams{TgId: &playerByUsername.TgID, TgUsername: &playerByUsername.TgUsername})
		} else {
			infra.Errorf(ctx, "Internal server error while trying to get player by tg_username %v: %v, resulsts doesn't match", request.TgUsername, err)
			return InternalErrorResponse(ectx, err.Error())
		}

	}
	return ectx.String(http.StatusBadRequest, "Invalid request body")
}
