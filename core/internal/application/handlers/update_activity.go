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
	UpdateActivityService interface {
		UpdateActivity(ctx context.Context, activityID int64, title, description *string, sportSectionID, creatorID *int64) (*dto.Activity, error)
	}

	UpdateActivityHandler struct {
		updateActivityService UpdateActivityService
	}
)

func NewUpdateActivityHandler(
	updateActivityService UpdateActivityService,
) *UpdateActivityHandler {
	return &UpdateActivityHandler{
		updateActivityService: updateActivityService,
	}
}

func (h *UpdateActivityHandler) UpdateActivity(ectx echo.Context, id int64, params server.PostCoreActivityUpdateByIdParams) error {
	ctx := context.Background()
	infra.Infof(ctx, "Processing UpdateActivity handler for activity ID: %d", id)

	if len(params.PrivilegeToken) == 0 {
		infra.Errorf(ctx, "Privilege token is required")
		return UnauthorizedErrorResponsef(ectx, "Privilege token is required")
	}

	var requestBody server.PostCoreActivityUpdateByIdJSONRequestBody
	if err := ectx.Bind(&requestBody); err != nil {
		infra.Errorf(ctx, "Invalid request body: %v", err)
		return BadRequestErrorResponsef(ectx, "Invalid request body: %s", err.Error())
	}

	activity, err := h.updateActivityService.UpdateActivity(ctx, id, requestBody.Title, requestBody.Description, requestBody.SportSectionId, requestBody.CreatorId)
	if err != nil {
		infra.Errorf(ctx, "Internal server error while trying to update activity: %v", err)
		return InternalErrorResponsef(ectx, err.Error())
	}

	resultActivity := mappers.MapActivityToAPI(*activity)
	return ectx.JSON(200, server.ActivityResponse{
		Activity: resultActivity,
	})
}
