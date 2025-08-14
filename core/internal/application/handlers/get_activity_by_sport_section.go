package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
	domain "match/internal/domain/dao"
	"match/internal/generated/server"
	"match/internal/infra"
)

type (
	GetActivitiesBySportSectionID interface {
		GetActivitiesBySportSectionID(ctx context.Context, sportSectionID int64) ([]domain.Activity, []domain.Player, error)
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
	activities, activityCreators, err := h.activityService.GetActivitiesBySportSectionID(ctx, id)
	if err != nil {
		infra.Errorf(ctx, "Internal server error while trying to find activity: %v", err)
		return InternalErrorResponse(ectx, err.Error())
	}

	infra.Infof(ctx, "%d activities have been found and extracted succesfully", len(activities))

	var resultActivities []server.Activity
	for activityIndex, activity := range activities {
		activityCreator := activityCreators[activityIndex]
		resultActivityCreator := server.Player{CoreId: activityCreator.ID, TgId: activityCreator.TgID}
		resultActivity := server.Activity{Id: activity.ID, Title: activity.Title, Description: &activity.Description, Creator: resultActivityCreator}

		resultActivities = append(resultActivities, resultActivity)
	}

	return ectx.JSON(200, server.ActivityListResponse{
		Activities: resultActivities,
	})
}
