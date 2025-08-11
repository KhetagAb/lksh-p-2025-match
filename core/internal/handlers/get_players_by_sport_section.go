package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
)

type (
	GetPlayersBySportSectionService interface {
		GetPlayersBySportSection(ctx context.Context, section string) ([]string, error)
	}

	GetPlayersBySportSectionHandler struct {
		getPlayersBySportSectionService GetPlayersBySportSectionService
	}
)

func (h *GetPlayersBySportSectionHandler) GetPlayersBySportSection(ectx echo.Context) error {
	ctx := context.Background()
	//logger.Infof(ctx, "Validating player username: %v", tgUsername)
	section := ectx.Param("section")
	allPlayers, err := h.getPlayersBySportSectionService.GetPlayersBySportSection(ctx, section)

	if err != nil {
		//logger.Errorf(ctx, "Internal server error while trying to find %v: %v", tgUsername, err)
		return ectx.JSON(500, err)
	}
	//logger.Infof(ctx, "Player %v has been found succesfully", tgUsername)
	return ectx.JSON(200, allPlayers)
}
