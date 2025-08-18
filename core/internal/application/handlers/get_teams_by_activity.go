package handlers

import (
	"context"
	"match/internal/application/handlers/mappers"
	"match/internal/domain/dto"
	"match/internal/generated/server"
	"match/internal/infra"

	"github.com/labstack/echo/v4"
)

type (
	GetTeamsByActivityID interface {
		GetTeamsByActivityID(ctx context.Context, id int64) (dto.Teams, error)
	}

	GetTeamsByActivityIDHandler struct {
		teamService GetTeamsByActivityID
	}
)

func NewGetTeamsByActivityIDHandler(
	teamService GetTeamsByActivityID,
) *GetTeamsByActivityIDHandler {
	return &GetTeamsByActivityIDHandler{
		teamService: teamService,
	}
}

func (h *GetTeamsByActivityIDHandler) GetTeamsByActivityID(ectx echo.Context, activityID int64) error {
	ctx := context.Background()

	infra.Infof(ctx, "Getting activity by ID=%d", activityID)
	teamsDTO, err := h.teamService.GetTeamsByActivityID(ctx, activityID)
	if err != nil {
		infra.Errorf(ctx, "Internal server error while trying to find activity: %v", err)
		return InternalErrorResponse(ectx, err.Error())
	}
	infra.Infof(ctx, "%d teams have been found and extracted succesfully", 1)

	resultTeams := server.TeamList{}

	for _, teamDTO := range teamsDTO {
		//teamPlayers := teamDTO.Players
		//resultTeamPlayers := server.PlayerList{}
		//
		//for _, player := range teamPlayers {
		//	resultTeamPlayer := server.Player{
		//		CoreId: player.ID,
		//		TgId:   player.TgID,
		//	}
		//	resultTeamPlayers = append(resultTeamPlayers, resultTeamPlayer)
		//}
		//
		//teamCaptain := teamDTO.Captain
		//resultTeamCaptain := server.Player{
		//	CoreId: teamCaptain.ID,
		//	TgId:   teamCaptain.TgID,
		//}

		resultTeam := mappers.MapTeamToAPI(teamDTO)
		resultTeams = append(resultTeams, resultTeam)
	}

	return ectx.JSON(200, server.ActivityTeamsResponse{
		Teams: resultTeams,
	})
}
