package teams

import (
	"context"
	"fmt"
	"match/internal/domain/dto"
)

func (s *TeamService) GetTeamsByActivityID(ctx context.Context, activityID int64) (dto.Teams, error) {
	teams, err := s.teamRepository.GetTeamsByActivityID(ctx, activityID)
	if err != nil {
		return nil, fmt.Errorf("cannot get teams by activity_id [activity_id=%d]: %w", activityID, err)
	}

	var teamsDTO dto.Teams
	for _, team := range teams {
		teamCaptain, err := s.playerRepository.GetPlayerByID(ctx, team.CaptainID)
		if err != nil {
			return nil, fmt.Errorf("cannot get captain player by player_id [player_id=%d]: %w", team.CaptainID, err)
		}

		teamPlayers, err := s.teamRepository.GetTeamPlayersByID(ctx, team.ID)
		if err != nil {
			return nil, fmt.Errorf("cannot get members players by team_id [team_id=%d]: %w", team.ID, err)
		}

		teamDTO := dto.Team{Team: team, Captain: *teamCaptain, Players: teamPlayers}

		teamsDTO = append(teamsDTO, teamDTO)
	}

	return teamsDTO, nil
}
