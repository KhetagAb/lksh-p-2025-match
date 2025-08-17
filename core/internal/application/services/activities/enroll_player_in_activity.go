package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dao"
	"match/internal/domain/services"
)

func (s *ActivityService) EnrollPlayerInActivity(ctx context.Context, activityID, playerTgID int64) (*dao.Team, error) {
	// Checking existance of given Activity
	_, err := s.activityRepository.GetActivityByID(ctx, activityID)
	if err != nil {
		return nil, fmt.Errorf("cannot get activity by id [activity_id=%d]: %w", activityID, err)
	}

	// Checking existance and getting info by tg_id
	captain, err := s.playerRepository.GetPlayerByTgID(ctx, playerTgID)
	if err != nil {
		return nil, fmt.Errorf("cannot get player by tg_id [player_tg_id=%d]: %w", playerTgID, err)
	}

	existingTeam, err := s.teamRepository.GetTeamByPlayerAndActivity(ctx, captain.ID, activityID)
	if err == nil && existingTeam != nil {
		return nil, &services.InvalidOperationError{
			Code:    services.InvalidOperation,
			Message: fmt.Sprintf("player already enrolled in team for this activity [player_id=%d][activity_id=%d][team_id=%d]", captain.ID, activityID, existingTeam.ID),
		}
	}

	// Creating team
	teamID, err := s.teamRepository.CreateTeam(ctx, captain.Name, captain.ID, activityID)
	if err != nil {
		return nil, fmt.Errorf("cannot create team using given name, captain_id and activity_id [name=%s][captain_id=%d][activity_id=%d]", captain.Name, captain.ID, activityID)
	}

	err = s.teamRepository.AddPlayerToTeam(ctx, captain.ID, *teamID)
	if err != nil {
		return nil, fmt.Errorf("cannot add captain to team [team_id=%d][team_name=%s][team_captain_id=%d][team_activity_id=%d]: %v", *teamID, captain.Name, captain.ID, activityID, err)
	}

	result := dao.Team{ID: *teamID, Name: captain.Name, CaptainID: captain.ID, ActivityID: activityID}

	return &result, nil
}
