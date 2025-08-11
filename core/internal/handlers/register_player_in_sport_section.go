package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
)

type (
	RegisterPlayerInSportSectionService interface {
		RegisterPlayerInSportSection(ctx context.Context, id int) (string, error)
	}

	RegisterPlayerInSportSectionHandler struct {
		RegisterPlayerInSportSectionService RegisterPlayerInSportSectionService
	}
)

func (h *RegisterPlayerInSportSectionHandler) RegisterPlayerInSportSection(ectx echo.Context) error {
	ctx := context.Background()
	//logger.Infof(ctx, "Validating player username: %v", tgUsername)
	id := 1 // TODO
	status, err := h.RegisterPlayerInSportSectionService.RegisterPlayerInSportSection(ctx, id)

	if err != nil {
		//logger.Errorf(ctx, "Internal server error while trying to find %v: %v", tgUsername, err)
		return ectx.JSON(500, err)
	}
	//logger.Infof(ctx, "Player %v has been found succesfully", tgUsername)
	return ectx.JSON(200, status)
}
