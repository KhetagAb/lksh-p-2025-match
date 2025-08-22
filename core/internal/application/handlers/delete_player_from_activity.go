package handlers

import (
	"context"
	"errors"
	"github.com/labstack/echo/v4"

	"match/internal/domain/services"
	"match/internal/generated/server"
	"match/internal/infra"
)

type (
	DeletePlayerFromActivity interface {
		DeletePlayerFromActivity(ctx context.Context, activityID, playerTgID int64) error
	}

	DeletePlayerFromActivityHandler struct {
		activityService DeletePlayerFromActivity
	}
)

func NewDeletePlayerFromActivityHandler(
	activityService DeletePlayerFromActivity,
) *DeletePlayerFromActivityHandler {
	return &DeletePlayerFromActivityHandler{
		activityService: activityService,
	}
}

func (h *DeletePlayerFromActivityHandler) DeletePlayerFromActivity(ectx echo.Context, activityId int64) error {
	ctx := context.Background()

	var requestBody server.PostCoreActivityIdEnrollJSONRequestBody
	if err := ectx.Bind(&requestBody); err != nil {
		return BadRequestErrorResponsef(ectx, "Invalid request body: %s", err.Error())
	}

	infra.Infof(ctx, "Deleting player [id=%d] from activity activity [id=%d]", requestBody.Id, activityId)
	err := h.activityService.DeletePlayerFromActivity(ctx, activityId, requestBody.Id)
	if err != nil {
		var invalidOpErr *services.InvalidOperationError
		if errors.As(err, &invalidOpErr) {
			infra.Warnf(ctx, "Player [id=%d] is not enrolled in activity [id=%d]: %v", requestBody.Id, activityId, err)
			return NotFoundErrorResponsef(ectx, "Player [id=%d] is not enrolled in activity [id=%d]: %v", requestBody.Id, activityId, err)
		}

		infra.Errorf(ctx, "Internal server error while trying to delete player [id=%d] from activity [id=%d]: %v", requestBody.Id, activityId, err)
		return InternalErrorResponsef(ectx, err.Error())
	}

	infra.Infof(ctx, "Player id=%d succesfully deleted from activity=%d", requestBody.Id, activityId)
	// TODO вернуть только 200
	return ectx.String(200, "")
}
