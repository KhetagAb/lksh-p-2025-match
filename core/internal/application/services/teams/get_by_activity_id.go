package teams

import (
	"context"
	"fmt"
	"match/internal/domain/dao"
)

func (s *TeamService) GetTeamsByActivityID(ctx context.Context, activityID int64) ([]dao.Team, []dao.Player, [][]dao.Player, error) {
	teams, err := s.teamRepository.GetTeamsByActivityID(ctx, activityID)
	if err != nil {
		return nil, nil, nil, fmt.Errorf("cannot get teams by activity_id [activity_id=%d]: %w", activityID, err)
	}

	teamCaptains := []dao.Player{}
	teamsPlayers := [][]dao.Player{}
	for _, team := range teams {
		// Getting team captain
		{
			teamCaptain, err := s.playerRepository.GetPlayerByID(ctx, team.CaptainID)
			if err != nil {
				return nil, nil, nil, fmt.Errorf("cannot get captain player by player_id [player_id=%d]: %w", team.CaptainID, err)
			}

			teamCaptains = append(teamCaptains, *teamCaptain)
		}

		// Getting team members
		{
			teamPlayers, err := s.teamRepository.GetTeamPlayersByID(ctx, team.ID)
			if err != nil {
				return nil, nil, nil, fmt.Errorf("cannot get members players by team_id [team_id=%d]: %w", team.ID, err)
			}

			teamsPlayers = append(teamsPlayers, teamPlayers)
		}
	}

	return teams, teamCaptains, teamsPlayers, nil
}
