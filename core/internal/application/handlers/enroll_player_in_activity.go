package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
	"match/internal/domain/dao"
	"match/internal/generated/presentation"
	"match/internal/infra"
)

type (
	EnrollPlayerInActivity interface {
		EnrollPlayerInActivity(ctx context.Context, activityID, playerTgID int64) (*dao.Team, error)
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

	var requestBody presentation.PostCoreActivityIdEnrollJSONRequestBody

	if err := ectx.Bind(&requestBody); err != nil {
		return ectx.JSON(400, &presentation.ErrorResponse{
			Message: "Invalid request body: " + err.Error(),
		})
	}

	if requestBody.TgId == nil {
		return ectx.JSON(400, &presentation.ErrorResponse{
			Message: "TgId is required",
		})
	}

	infra.Infof(ctx, "Creating Team by tgID (%d)", id)
	domainTeam, err := h.activityService.EnrollPlayerInActivity(ctx, id, *requestBody.TgId)
	if err != nil {
		infra.Errorf(ctx, "Internal server error while trying to create team: %v", err)
		return InternalErrorResponse(ectx, err.Error())
	}

	infra.Infof(ctx, "Team created successfully [team_id=%d][team_name=%s][team_captain_id=%d][activity_id=%d]",
		domainTeam.ID, domainTeam.Name, domainTeam.CaptainID, domainTeam.ActivityID)

	player := presentation.Player{
		CoreId: domainTeam.CaptainID,
		TgId:   *requestBody.TgId,
	}

	resultTeam := presentation.Team{
		Id:      domainTeam.ID,
		Name:    domainTeam.Name,
		Members: []presentation.Player{player},
		Captain: player,
	}

	return ectx.JSON(200, resultTeam)
}
