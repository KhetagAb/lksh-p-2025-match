package handlers

import (
	"context"
	"match/domain"
	"match/internal/generated/server"
	"match/pkg/logger"

	"github.com/labstack/echo/v4"
)

type (
	GetActivityBySportSectionID interface {
		GetActivityBySportSectionID(ctx context.Context, sportSectionID int64) ([]domain.Activity, []domain.Player, error)
	}

	GetActivityBySportSectionIDHandler struct {
		activityService GetActivityBySportSectionID
	}
)

func NewGetActivityBySportSectionIDHandler(
	activityService GetActivityBySportSectionID,
) *GetActivityBySportSectionIDHandler {
	return &GetActivityBySportSectionIDHandler{
		activityService: activityService,
	}
}

func (h *GetActivityBySportSectionIDHandler) GetActivityBySportSectionID(ectx echo.Context, id int64) error {
	ctx := context.Background()
	logger.Infof(ctx, "Getting ActivityList by SportSection ID (%d)", id)
	domainActivityList, domainCreatorList, err := h.activityService.GetActivityBySportSectionID(ctx, id)
	if err != nil {
		logger.Errorf(ctx, "Internal server error while trying to find activity: %v", err)
		return InternalErrorResponse(ectx, err.Error())
	}

	logger.Infof(ctx, "%d activities have been found and extracted succesfully", len(domainActivityList))

	var activities []server.Activity
	for index, activity := range domainActivityList {
		domainCreator := domainCreatorList[index]
		resultActivityCreator := server.Player{CoreId: domainCreator.ID, TgId: domainCreator.TgID}
		resultActivity := server.Activity{Id: activity.ID, Title: activity.Title, Description: &activity.Description, Creator: resultActivityCreator}

		activities = append(activities, resultActivity)
	}

	return ectx.JSON(200, server.ActivityListResponse{
		Activities: activities,
	})
}
