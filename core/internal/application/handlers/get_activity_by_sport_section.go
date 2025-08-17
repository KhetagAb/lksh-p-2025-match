package handlers

import (
	"context"
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

	resultActivities := []server.Activity{}
	for _, activityDTO := range activitiesDTO {
		activityCreator := activityDTO.Creator
		resultActivityCreator := server.Player{CoreId: activityCreator.ID, TgId: activityCreator.TgID}
		resultActivity := server.Activity{Id: activityDTO.Activity.ID, Title: activityDTO.Activity.Title, Description: &activityDTO.Activity.Description, Creator: resultActivityCreator}

		resultActivities = append(resultActivities, resultActivity)
	}

	return ectx.JSON(200, server.ActivityListResponse{
		Activities: resultActivities,
	})
}
