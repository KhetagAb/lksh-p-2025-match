package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dao"
	"match/internal/domain/dto"
	"match/internal/domain/services"
	"match/internal/infra"
)

func (s *ActivityService) EnrollPlayerInActivity(ctx context.Context, activityID, playerTgID int64) (*dto.Team, error) {
	infra.Infof(ctx, "Enrolling player with tg_id=%v in activity with id=%v", playerTgID, activityID)

	infra.Infof(ctx, "Getting activity with id=%v", activityID)
	_, err := s.activityRepository.GetActivityByID(ctx, activityID)
	if err != nil {
		return nil, fmt.Errorf("cannot get activity by id [activity_id=%d]: %w", activityID, err)
	}

	infra.Infof(ctx, "Getting player with tg_id=%v", playerTgID)
	captain, err := s.playerRepository.GetPlayerByTgID(ctx, playerTgID)
	if err != nil {
		return nil, fmt.Errorf("cannot get player by tg_id [player_tg_id=%d]: %w", playerTgID, err)
	}

	infra.Infof(ctx, "Getting team by player and activity [player_id=%d] [activity_id=%d]", captain.ID, activityID)
	existingTeam, err := s.teamRepository.GetTeamByPlayerAndActivity(ctx, captain.ID, activityID)
	if err == nil && existingTeam != nil {
		return nil, &services.InvalidOperationError{
			Code:    services.InvalidOperation,
			Message: fmt.Sprintf("player already enrolled in team for this activity with player_id=%d, activity_id=%d, team_id=%d", captain.ID, activityID, existingTeam.ID),
		}
	}

	infra.Infof(ctx, "Creating team [name=%s] [captain_id=%d] [activity_id=%d]", captain.Name, captain.ID, activityID)
	teamID, err := s.teamRepository.CreateTeam(ctx, captain.Name, captain.ID, activityID)
	if err != nil {
		return nil, fmt.Errorf("cannot create team with name=%s, captain_id=%d, activity_id=%d", captain.Name, captain.ID, activityID)
	}

	infra.Infof(ctx, "Adding player to team [player_id=%d] [team_id=%d]", captain.ID, *teamID)
	err = s.teamRepository.AddPlayerToTeam(ctx, captain.ID, *teamID)
	if err != nil {
		return nil, fmt.Errorf("cannot add captain to team with team_id=%d: %v", *teamID, err)
	}

	result := dto.Team{Team: dao.Team{ID: *teamID, CaptainID: captain.ID, Name: captain.Name, ActivityID: activityID}, Captain: *captain, Players: []dao.Player{*captain}}

	infra.Infof(ctx, "Player enrolled in activity successfully [player_id=%d] [activity_id=%d]", captain.ID, activityID)
	return &result, nil
}
