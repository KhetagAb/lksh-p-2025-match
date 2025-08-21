package handlers

import (
	"context"
	"match/internal/application/handlers/mappers"
	"match/internal/domain/dao"
	"match/internal/domain/dto"
	"match/internal/generated/server"
	"match/internal/infra"

	"github.com/labstack/echo/v4"
)

type (
	CreateActivityService interface {
		CreateActivity(ctx context.Context, activity dao.Activity) (*dto.Activity, error)
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

func (h *CreateActivityHandler) CreateActivity(ectx echo.Context, params server.PostCoreActivityCreateParams) error {
	ctx := context.Background()
	infra.Infof(ctx, "Processing CreateActivity handler with params: %+v", params)

	if len(params.PrivilegeToken) == 0 {
		infra.Errorf(ctx, "Privilege token is required")
		return UnauthorizedErrorResponsef(ectx, "Privilege token is required")
	}

	var requestBody server.PostCoreActivityCreateJSONRequestBody
	if err := ectx.Bind(&requestBody); err != nil {
		infra.Errorf(ctx, "Invalid request body: %v", err)
		return BadRequestErrorResponsef(ectx, "Invalid request body: "+err.Error())
	}

	activity, err := h.createActivityService.CreateActivity(ctx,
		mappers.MapActivityFromAPI(requestBody),
	)
	if err != nil {
		infra.Errorf(ctx, "Internal server error while trying to create activity: %v", err)
		return InternalErrorResponsef(ectx, err.Error())
	}

	resultActivity := mappers.MapActivityToAPI(*activity)
	return ectx.JSON(200, server.ActivityResponse{
		Activity: resultActivity,
	})
}
