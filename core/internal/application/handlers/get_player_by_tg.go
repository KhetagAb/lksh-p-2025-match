package handlers

import (
	"context"
	"match/internal/application/handlers/mappers"
	"match/internal/domain/dao"
	"match/internal/generated/server"
	"match/internal/infra"

	"github.com/labstack/echo/v4"
)

type (
	GetPlayerByTgService interface {
		GetPlayerByTgID(ctx context.Context, telegramID int64) (*dao.Player, error)
		GetPlayerByTgUsername(ctx context.Context, telegramUsername string) (*dao.Player, error)
	}

	GetPlayerByTgHandler struct {
		playerService GetPlayerByTgService
	}
)

func NewGetPlayerByTgHandler(
	playerService GetPlayerByTgService,
) *GetPlayerByTgHandler {
	return &GetPlayerByTgHandler{
		playerService: playerService,
	}
}

func (h *GetPlayerByTgHandler) GetPlayerByTg(ectx echo.Context, params server.GetCorePlayerByTgParams) error {
	if params.TgId == nil && params.TgUsername == nil {
		return BadRequestErrorResponsef(ectx, "Either tg_id or tg_username must be provided")
	}
	if params.TgId != nil && params.TgUsername != nil {
		return BadRequestErrorResponsef(ectx, "Only one of tg_id or tg_username must be provided")
	}

	ctx := context.Background()
	var player *dao.Player
	var err error
	if params.TgId != nil {
		infra.Infof(ctx, "Getting player by tg_id=%d", *params.TgId)
		player, err = h.playerService.GetPlayerByTgID(ctx, *params.TgId)
		if err != nil {
			infra.Errorf(ctx, "Error getting player by tg_id %d: %v", *params.TgId, err)
			return InternalErrorResponsef(ectx, "Error getting player by tg_id %d: %v", *params.TgId, err)
		}
		if player == nil {
			return NotFoundErrorResponsef(ectx, "Player not found with tg_id %d", *params.TgId)
		}
	} else {
		infra.Infof(ctx, "Getting player by tg_username=%s", *params.TgUsername)
		player, err = h.playerService.GetPlayerByTgUsername(ctx, *params.TgUsername)
		if err != nil {
			infra.Errorf(ctx, "Error getting player by tg_username %s: %v", *params.TgUsername, err)
			return InternalErrorResponsef(ectx, "Error getting player by tg_username %s: %v", *params.TgUsername, err)
		}
		if player == nil {
			return NotFoundErrorResponsef(ectx, "Player not found with tg_username %s", *params.TgUsername)
		}
	}

	response := mappers.MapPlayerToAPI(*player)
	return ectx.JSON(200, server.PlayerResponse{Player: response})
}
