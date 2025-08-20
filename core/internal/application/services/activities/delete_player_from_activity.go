package activities

import (
	"context"
	"fmt"
	"match/internal/domain/services"
	"match/internal/infra"
)

func (s *ActivityService) DeletePlayerFromActivity(ctx context.Context, activityID, playerID int64) error {
	infra.Infof(ctx, "Deleting player with id=%v from activity with id=%v", playerID, activityID)

	infra.Infof(ctx, "Getting activity with id=%v", activityID)
	_, err := s.activityRepository.GetActivityByID(ctx, activityID)
	if err != nil {
		return fmt.Errorf("cannot get activity by activity_id=%d: %w", activityID, err)
	}

	infra.Infof(ctx, "Getting player with id=%v", playerID)
	captain, err := s.playerService.GetPlayerByID(ctx, playerID)
	if err != nil {
		return fmt.Errorf("cannot get player by id=%v: %w", playerID, err)
	}

	infra.Infof(ctx, "Getting team by player and activity [player_id=%d] [activity_id=%d]", captain.ID, activityID)
	existingTeam, err := s.teamRepository.GetTeamByPlayerAndActivity(ctx, captain.ID, activityID)
	if err != nil {
		return &services.InvalidOperationError{
			Code:    services.InvalidOperation,
			Message: fmt.Sprintf("player isn't enrolled in team for this activity with player_id=%d, activity_id=%d", captain.ID, activityID),
		}
	}

	infra.Infof(ctx, "Deleting player [id=%d] from activity [id=%d]", playerID, activityID)
	err = s.teamRepository.DeletePlayerFromTeamByActivity(ctx, playerID, existingTeam.ID)
	if err != nil {
		return fmt.Errorf("cannot delete player with id=%d from activity id=%d: %v", playerID, activityID, err)
	}

	infra.Infof(ctx, "Player deleted from activity successfully [player_id=%d] [activity_id=%d]", playerID, activityID)
	return nil
}
