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
	GetActivitiesBySportSectionID interface {
		GetActivitiesBySportSectionID(ctx context.Context, sportSectionID int64) (dto.Activities, error)
	}

	GetActivitiesBySportSectionIDHandler struct {
		activityService GetActivitiesBySportSectionID
	}
)

func NewGetActivitiesBySportSectionIDHandler(
	activityService GetActivitiesBySportSectionID,
) *GetActivitiesBySportSectionIDHandler {
	return &GetActivitiesBySportSectionIDHandler{
		activityService: activityService,
	}
}

func (h *GetActivitiesBySportSectionIDHandler) GetActivitiesBySportSectionID(ectx echo.Context, id int64) error {
	ctx := context.Background()
	infra.Infof(ctx, "Getting activities by SportSection ID (%d)", id)
	activitiesDTO, err := h.activityService.GetActivitiesBySportSectionID(ctx, id)
	if err != nil {
		infra.Errorf(ctx, "Internal server error while trying to find activity: %v", err)
		return InternalErrorResponse(ectx, err.Error())
	}

	infra.Infof(ctx, "%d activities have been found and extracted succesfully", len(activitiesDTO))

	var resultActivities []server.Activity
	for _, activityDTO := range activitiesDTO {

		resultActivities = append(resultActivities, mappers.MapActivityToAPI(activityDTO))
	}

	return ectx.JSON(200, server.ActivityListResponse{
		Activities: resultActivities,
	})
}
