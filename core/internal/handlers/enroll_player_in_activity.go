package handlers

import (
	"context"
	"match/domain"
	"match/internal/generated/server"
	"match/pkg/logger"

	"github.com/labstack/echo/v4"
)

type (
	EnrollPlayerInActivity interface {
		EnrollPlayerInActivity(ctx context.Context, activityID, playerTgID int64) (*domain.Team, error)
	}

	EnrollPlayerInActivityHandler struct {
		activityService EnrollPlayerInActivity
	}
)

func NewEnrollPlayerInActivityHandler(
	activityService EnrollPlayerInActivity,
) *EnrollPlayerInActivityHandler {
	return &EnrollPlayerInActivityHandler{
		activityService: activityService,
	}
}

func (h *EnrollPlayerInActivityHandler) EnrollPlayerInActivity(ectx echo.Context, id int64) error {
	ctx := context.Background()

	var requestBody server.PostCoreActivityIdEnrollJSONRequestBody

	if err := ectx.Bind(&requestBody); err != nil {
		return ectx.JSON(400, &server.ErrorResponse{
			Message: "Invalid request body: " + err.Error(),
		})
	}

	if requestBody.TgId == nil {
		return ectx.JSON(400, &server.ErrorResponse{
			Message: "TgId is required",
		})
	}

	logger.Infof(ctx, "Creating Team by tgID (%d)", id)
	domainTeam, err := h.activityService.EnrollPlayerInActivity(ctx, id, *requestBody.TgId)
	if err != nil {
		logger.Errorf(ctx, "Internal server error while trying to create team: %v", err)
		return InternalErrorResponse(ectx, err.Error())
	}

	logger.Infof(ctx, "Team created successfully [team_id=%d][team_name=%s][team_captain_id=%d][activity_id=%d]",
		domainTeam.ID, domainTeam.Name, domainTeam.CaptainID, domainTeam.ActivityID)

	player := server.Player{
		CoreId: domainTeam.CaptainID,
		TgId:   *requestBody.TgId,
	}

	resultTeam := server.Team{
		Id:      domainTeam.ID,
		Name:    domainTeam.Name,
		Members: []server.Player{player},
		Captain: player,
	}

	return ectx.JSON(200, resultTeam)
}
