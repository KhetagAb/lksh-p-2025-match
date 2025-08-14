package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
	domain "match/internal/domain/dao"
	"match/internal/generated/server"
	"match/internal/infra"
)

type (
	GetTeamsByActivityID interface {
		GetTeamsByActivityID(ctx context.Context, id int64) ([]domain.Team, []domain.Player, [][]domain.Player, error)
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
	teams, captains, players, err := h.teamService.GetTeamsByActivityID(ctx, activityID)
	if err != nil {
		infra.Errorf(ctx, "Internal server error while trying to find activity: %v", err)
		return InternalErrorResponse(ectx, err.Error())
	}
	infra.Infof(ctx, "%d teams have been found and extracted succesfully", 1)

	resultTeams := server.TeamList{}

	// Mapping teams
	{
		for teamIndex, team := range teams {
			// Mapping players
			teamPlayers := players[teamIndex]
			resultTeamPlayers := server.PlayerList{}

			for _, player := range teamPlayers {
				resultTeamPlayer := server.Player{
					CoreId: player.ID,
					TgId:   player.TgID,
				}
				resultTeamPlayers = append(resultTeamPlayers, resultTeamPlayer)
			}

			// Mapping captain
			teamCaptain := captains[teamIndex]
			resultTeamCaptain := server.Player{
				CoreId: teamCaptain.ID,
				TgId:   teamCaptain.TgID,
			}

			resultTeam := server.Team{
				Id:      team.ID,
				Name:    team.Name,
				Captain: resultTeamCaptain,
				Members: resultTeamPlayers,
			}

			resultTeams = append(resultTeams, resultTeam)
		}
	}

	return ectx.JSON(200, server.ActivityTeamsResponse{
		Teams: resultTeams,
	})
}
