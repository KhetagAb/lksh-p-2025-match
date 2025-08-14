package handlers

import (
	"context"
	"match/domain"
	"match/internal/generated/server"
	"match/pkg/logger"

	"github.com/labstack/echo/v4"
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
	logger.Infof(ctx, "Getting activities by SportSection ID (%d)", id)
	activities, activityCreators, err := h.activityService.GetActivitiesBySportSectionID(ctx, id)
	if err != nil {
		logger.Errorf(ctx, "Internal server error while trying to find activity: %v", err)
		return InternalErrorResponse(ectx, err.Error())
	}

	logger.Infof(ctx, "%d activities have been found and extracted succesfully", len(activities))

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
