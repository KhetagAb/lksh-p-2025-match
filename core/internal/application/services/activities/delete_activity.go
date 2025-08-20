package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dto"
	"match/internal/infra"
)

func (s *ActivityService) DeleteActivity(ctx context.Context, activityID int64) (*dto.Activity, error) {
	infra.Infof(ctx, "Getting activity to delete with id=%v", activityID)

	existingActivity, err := s.activityRepository.GetActivityByID(ctx, activityID)
	if err != nil {
		return nil, fmt.Errorf("cannot get activity by id [activity_id=%d]: %w", activityID, err)
	}

	infra.Infof(ctx, "Getting creator player with id=%v", existingActivity.CreatorID)
	creator, err := s.playerService.GetPlayerByID(ctx, existingActivity.CreatorID)
	if err != nil {
		return nil, fmt.Errorf("cannot get player by id [player_id=%d]: %w", existingActivity.CreatorID, err)
	}

	infra.Infof(ctx, "Deleting activity with id=%d", activityID)
	deletedActivity, err := s.activityRepository.DeleteActivity(ctx, activityID)
	if err != nil {
		return nil, fmt.Errorf("cannot delete activity with id=%d: %w", activityID, err)
	}

	infra.Infof(ctx, "Activity deleted: [activity=%v]", deletedActivity)
	return &dto.Activity{Activity: *deletedActivity, Creator: *creator}, nil
}
