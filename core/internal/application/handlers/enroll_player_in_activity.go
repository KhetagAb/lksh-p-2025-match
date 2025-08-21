package handlers

import (
	"context"
	"errors"
	"github.com/labstack/echo/v4"
	"match/internal/application/handlers/mappers"
	"match/internal/domain/dto"
	"match/internal/domain/services"
	"match/internal/generated/server"
	"match/internal/infra"
)

type (
	EnrollPlayerInActivity interface {
		EnrollPlayerInActivity(ctx context.Context, activityID, playerTgID int64) (*dto.Team, error)
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
		return BadRequestErrorResponsef(ectx, "Invalid request body: %s", err.Error())
	}

	infra.Infof(ctx, "Creating Team in activity [id=%d]", id)
	team, err := h.activityService.EnrollPlayerInActivity(ctx, id, requestBody.Id)
	if err != nil {
		var invalidOpErr *services.InvalidOperationError
		var forbiddenOpErr *services.ForbiddenOperationError
		if errors.As(err, &invalidOpErr) {
			infra.Warnf(ctx, "Player already enrolled in activity: %v", err)
			return ConflictErrorResponsef(ectx, "Player is already enrolled in a team for this activity")
		}
		if errors.As(err, &forbiddenOpErr) {
			infra.Warnf(ctx, "Deadline to enroll in activity has expired: %v", err)
			return ForbiddenErrorResponsef(ectx, "Deadline to enroll in activity has expired")
		}

		infra.Errorf(ctx, "Internal server error while trying to create team: %v", err)
		return InternalErrorResponsef(ectx, err.Error())
	}

	infra.Infof(ctx, "Team created successfully [team_id=%d] [team_name=%s] [team_captain_id=%d]",
		team.Team.ID, team.Team.Name, team.Captain.ID)

	resultTeam := mappers.MapTeamToAPI(*team)
	return ectx.JSON(200, server.CreatedTeamResponse{
		Team: resultTeam,
	})
}
