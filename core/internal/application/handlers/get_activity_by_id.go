package handlers

import (
	"context"
	"match/internal/application/handlers/mappers"
	"match/internal/domain/dto"
	"match/internal/generated/server"
	"match/internal/infra"

	"github.com/labstack/echo/v4"
)

type (
	GetActivityByID interface {
		GetActivityByID(ctx context.Context, id int64) (*dto.Activity, error)
	}

	GetActivityByIDHandler struct {
		activityService GetActivityByID
	}
)

func NewGetActivityByIDHandler(
	activityService GetActivityByID,
) *GetActivityByIDHandler {
	return &GetActivityByIDHandler{
		activityService: activityService,
	}
}

func (h *GetActivityByIDHandler) GetActivityByID(ectx echo.Context, activityID int64) error {
	ctx := context.Background()

	infra.Infof(ctx, "Getting activity by ID=%d", activityID)
	activity, err := h.activityService.GetActivityByID(ctx, activityID)
	if err != nil {
		infra.Errorf(ctx, "Error while trying to find activity: %v", err)
		return NotFoundErrorResponsef(ectx, err.Error())
	}

	resultActivity := mappers.MapActivityToAPI(*activity)

	infra.Infof(ctx, "Activity with ID=%d has been found and extracted successfully", activityID)
	return ectx.JSON(200, server.ActivityResponse{
		Activity: resultActivity,
	})
}
