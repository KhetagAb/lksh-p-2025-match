package handlers

import (
	"context"
	"errors"
	"github.com/labstack/echo/v4"
	"match/internal/application/handlers/mappers"
	"match/internal/domain/dto"
	"match/internal/domain/services"
	"match/internal/generated/server"
	"match/internal/infra"
)

type (
	CreateActivityService interface {
		CreateActivity(ctx context.Context, creatorID, sportSectionId int64, title, description string) (*dto.Activity, error)
	}

	CreateActivityHandler struct {
		createActivityService CreateActivityService
	}
)

func NewCreateActivityHandler(
	createActivityService CreateActivityService,
) *CreateActivityHandler {
	return &CreateActivityHandler{
		createActivityService: createActivityService,
	}
}

func (h *CreateActivityHandler) CreateActivity(ectx echo.Context, id int64) error {
	ctx := context.Background()

	var requestBody server.PostCoreActivityCreateJSONRequestBody

	if err := ectx.Bind(&requestBody); err != nil {
		return ectx.JSON(400, &server.ErrorResponse{
			Message: "Invalid request body: " + err.Error(),
		})
	}

	//infra.Infof(ctx, "Creating Team by tgID (%d)", id)
	activity, err := h.createActivityService.CreateActivity(ctx, requestBody.CreatorId, requestBody.SportSectionId, *requestBody.Description, requestBody.Title)
	if err != nil {
		var invalidOpErr *services.InvalidOperationError
		if errors.As(err, &invalidOpErr) {
			infra.Warnf(ctx, "Activity already exists: %v", err)
			return ConflictErrorResponse(ectx, "Activity already exists")
		}

		infra.Errorf(ctx, "Internal server error while trying to create activity: %v", err)
		return InternalErrorResponse(ectx, err.Error())
	}

	resultActivity := mappers.MapActivityToAPI(*activity)
	infra.Infof(ctx, "Activity succesfully created: %v", resultActivity)

	return ectx.JSON(200, server.ActivityResponse{
		Activity: resultActivity,
	})
}
