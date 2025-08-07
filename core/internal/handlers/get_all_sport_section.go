package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
)

type (
	GetAllSportSectionService interface {
		GetAllSportSection(ctx context.Context) ([]string, error)
	}

	GetAllSportSectionHandler struct {
		getAllSportSectionService GetAllSportSectionService
	}
)

func (h *GetAllSportSectionHandler) GetAllSportSection(ectx echo.Context) error {
	ctx := context.Background()
	//logger.Infof(ctx, "Validating player username: %v", tgUsername)

	allSections, err := h.getAllSportSectionService.GetAllSportSection(ctx)

	if err != nil {
		//logger.Errorf(ctx, "Internal server error while trying to find %v: %v", tgUsername, err)
		return ectx.JSON(500, err)
	}
	//logger.Infof(ctx, "Player %v has been found succesfully", tgUsername)
	return ectx.JSON(200, allSections)
}
