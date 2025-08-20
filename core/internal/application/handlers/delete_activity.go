package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
	"match/internal/application/handlers/mappers"
	"match/internal/domain/dto"
	"match/internal/generated/server"
	"match/internal/infra"
)

type (
	DeleteActivityService interface {
		DeleteActivity(ctx context.Context, activityID int64) (*dto.Activity, error)
	}

	DeleteActivityHandler struct {
		deleteActivityService DeleteActivityService
	}
)

func NewDeleteActivityHandler(
	deleteActivityService DeleteActivityService,
) *DeleteActivityHandler {
	return &DeleteActivityHandler{
		deleteActivityService: deleteActivityService,
	}
}

func (h *DeleteActivityHandler) DeleteActivity(ectx echo.Context, id int64, params server.PostCoreActivityDeleteByIdParams) error {
	ctx := context.Background()
	infra.Infof(ctx, "Processing DeleteActivity handler for activity ID: %d", id)

	if len(params.PrivilegeToken) == 0 {
		infra.Errorf(ctx, "Privilege token is required")
		return UnauthorizedErrorResponsef(ectx, "Privilege token is required")
	}

	activity, err := h.deleteActivityService.DeleteActivity(ctx, id)
	if err != nil {
		infra.Errorf(ctx, "Internal server error while trying to delete activity: %v", err)
		return InternalErrorResponsef(ectx, err.Error())
	}

	resultActivity := mappers.MapActivityToAPI(*activity)
	return ectx.JSON(200, server.ActivityResponse{
		Activity: resultActivity,
	})
}
