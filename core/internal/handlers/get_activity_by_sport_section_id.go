package handlers

import (
	"context"
	"match/domain"
	"match/internal/generated/server"
	"match/pkg/logger"

	"github.com/labstack/echo/v4"
)

type (
	GetCoreActivityBySportSectionIDService interface {
		GetCoreActivityBySportSectionID(ctx context.Context, sportSectionID int64) ([]domain.Activity, []domain.Player, error)
	}

	GetCoreActivityBySportSectionIDHandler struct {
		getCoreActivityBySportSectionIDService GetCoreActivityBySportSectionIDService
	}
)

func NewGetCoreActivityBySportSectionIDHandler(
	getCoreActivityBySportSectionIDService GetCoreActivityBySportSectionIDService,
) *GetCoreActivityBySportSectionIDHandler {
	return &GetCoreActivityBySportSectionIDHandler{
		getCoreActivityBySportSectionIDService: getCoreActivityBySportSectionIDService,
	}
}

func (h *GetCoreActivityBySportSectionIDHandler) GetCoreActivityBySportSectionID(ectx echo.Context, id int64) error {
	ctx := context.Background()
	logger.Infof(ctx, "Getting ActivityList by SportSection ID (%d)", id)
	domainActivityList, domainCreatorList, err := h.getCoreActivityBySportSectionIDService.GetCoreActivityBySportSectionID(ctx, id)
	if err != nil {
		logger.Errorf(ctx, "Internal server error while trying to find activity: %v", err)
		return InternalErrorResponse(ectx, err.Error())
	}

	logger.Infof(ctx, "%d activities have been found and extracted succesfully", len(domainActivityList))

	var resultActivityList server.ActivityListResponse

	for index, activity := range domainActivityList {
		domainCreator := domainCreatorList[index]
		resultActivityCreator := server.Player{CoreId: domainCreator.ID, TgId: domainCreator.TgID}

		resultActivity := server.Activity{Id: activity.ID, Title: activity.Title, Description: &activity.Description, Creator: resultActivityCreator}

		resultActivityList = append(resultActivityList, resultActivity)
	}

	return ectx.JSON(200, resultActivityList)
}
