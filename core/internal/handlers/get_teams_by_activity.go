package handlers

import (
	"context"
	"match/domain"
	"match/internal/generated/server"
	"match/pkg/logger"

	"github.com/labstack/echo/v4"
)

type (
	GetTeamsByActivityID interface {
		GetCoreTeamsByActivityID(ctx context.Context, id int64) (*domain.Activity, *domain.Player, error)
	}

	GetTeamsByActivityIDHandler struct {
		activityService GetTeamsByActivityID
	}
)

func NewGetTeamsByActivityIDHandler(
	activityService GetTeamsByActivityID,
) *GetTeamsByActivityIDHandler {
	return &GetTeamsByActivityIDHandler{
		activityService: activityService,
	}
}

func (h *GetTeamsByActivityIDHandler) GetCoreActivityByID(ectx echo.Context, activityID int64) error {
	ctx := context.Background()

	logger.Infof(ctx, "Getting activity by ID=%d", activityID)
	domainActivity, domainCreator, err := h.activityService.GetCoreTeamsByActivityID(ctx, activityID)
	if err != nil {
		logger.Errorf(ctx, "Internal server error while trying to find activity: %v", err)
		return InternalErrorResponse(ectx, err.Error())
	}

	logger.Infof(ctx, "%d activities have been found and extracted succesfully", 1)

	resultActivityCreator := server.Player{CoreId: domainCreator.ID, TgId: domainCreator.TgID}
	resultActivity := server.Activity{Id: domainActivity.ID, Title: domainActivity.Title, Description: &domainActivity.Description, Creator: resultActivityCreator}

	return ectx.JSON(200, resultActivity)
}
