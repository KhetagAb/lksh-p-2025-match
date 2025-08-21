package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dto"
)

func (s *ActivityService) GetActivityByID(ctx context.Context, activityID int64) (*dto.Activity, error) {
	activity, err := s.activityRepository.GetActivityByID(ctx, activityID)
	if err != nil {
		return nil, fmt.Errorf("failed to get activity by id=%d: %w", activityID, err)
	}

	creator, err := s.playerService.GetPlayerByID(ctx, activity.CreatorID)
	if err != nil {
		return nil, fmt.Errorf("failed to get creator for activity id=%d: %w", activityID, err)
	}

	return &dto.Activity{
		Activity: *activity,
		Creator:  *creator,
	}, nil
}
