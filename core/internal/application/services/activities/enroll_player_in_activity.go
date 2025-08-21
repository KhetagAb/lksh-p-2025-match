package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dao"
	"match/internal/domain/dto"
	"match/internal/domain/services"
	"match/internal/infra"
	"time"
)

func (s *ActivityService) EnrollPlayerInActivity(ctx context.Context, activityID, playerID int64) (*dto.Team, error) {
	infra.Infof(ctx, "Enrolling player with_id=%v in activity with id=%v", playerID, activityID)

	infra.Infof(ctx, "Getting activity with id=%v", activityID)
	activity, err := s.activityRepository.GetActivityByID(ctx, activityID)
	if err != nil {
		return nil, fmt.Errorf("cannot get activity by activity_id=%d: %w", activityID, err)
	}

	if time.Now().UTC().After(*activity.EnrollDeadline) {
		infra.Infof(ctx, "Cannot create team because the enroll deadline has expired [activity_id=%v] [enroll_deadline=%v] [current time=%v]", activityID, activity.EnrollDeadline, time.Now().UTC())
		return nil, &services.ForbiddenOperationError{
			Code:    services.ForbiddenOperation,
			Message: fmt.Sprintf("cannot create team because the enroll deadline has expired [activity_id=%v] [enroll_deadline=%v] [current time=%v]: %w", activityID, activity.EnrollDeadline, time.Now().UTC()),
		}
	}
	infra.Infof(ctx, "Getting player with id=%v", playerID)
	captain, err := s.playerService.GetPlayerByID(ctx, playerID)
	if err != nil {
		return nil, fmt.Errorf("cannot get player by id=%v: %w", playerID, err)
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
