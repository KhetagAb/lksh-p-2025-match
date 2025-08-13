package handlers

import (
	"context"
	"match/domain"
	"match/internal/generated/server"
	"match/pkg/logger"

	"github.com/labstack/echo/v4"
)

type (
	GetCoreActivityByIDService interface {
		GetCoreActivityByID(ctx context.Context, id int64) (domain.Activity, domain.Player, error)
	}

	GetCoreActivityByIDHandler struct {
		getCoreActivityByIDService GetCoreActivityByIDService
	}
)

func NewGetCoreActivityByIDHandler(
	getCoreActivityByIDService GetCoreActivityByIDService,
) *GetCoreActivityByIDHandler {
	return &GetCoreActivityByIDHandler{
		getCoreActivityByIDService: getCoreActivityByIDService,
	}
}

func (h *GetCoreActivityByIDHandler) GetCoreActivityByID(ectx echo.Context, id int64) error {
	ctx := context.Background()
	logger.Infof(ctx, "Getting Activity by ID (%d)", id)
	domainActivity, domainCreator, err := h.getCoreActivityByIDService.GetCoreActivityByID(ctx, id)
	if err != nil {
		logger.Errorf(ctx, "Internal server error while trying to find activity: %v", err)
		return InternalErrorResponse(ectx, err.Error())
	}

	logger.Infof(ctx, "%d activities have been found and extracted succesfully", 1)

	resultActivityCreator := server.Player{CoreId: domainCreator.ID, TgId: domainCreator.TgID}
	resultActivity := server.Activity{Id: domainActivity.ID, Title: domainActivity.Title, Description: &domainActivity.Description, Creator: resultActivityCreator}

	return ectx.JSON(200, resultActivity)
}
