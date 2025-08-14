package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
	"match/domain"
	"match/internal/generated/server"
	"match/pkg/logger"
)

type (
	GetAllSportSectionService interface {
		GetAllSportSection(ctx context.Context) ([]domain.SportSection, error)
	}

	GetAllSportSectionHandler struct {
		getAllSportSectionService GetAllSportSectionService
	}
)

func (h *GetAllSportSectionHandler) GetAllSportSection(ectx echo.Context) error {
	ctx := context.Background()
	logger.Infof(ctx, "Trying to get the list of all sport sections")
	allSections, err := h.getAllSportSectionService.GetAllSportSection(ctx)
	if err != nil {
		logger.Infof(ctx, "An error occupied during getting the list of all sport sections: %v", err)
		return ectx.JSON(500, err)
	}
	logger.Infof(ctx, "The list of all sport sections has been succesfully received")
	var sliceOfSS []server.SportSection
	for _, el := range allSections {
		sliceOfSS = append(sliceOfSS, server.SportSection{Id: el.ID, Name: el.EnName, RuName: el.RuName})
	}
	return ectx.JSON(200, server.AllSportSections{
		SportsSections: sliceOfSS,
	})
}
