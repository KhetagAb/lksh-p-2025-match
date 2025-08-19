package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dto"
	"match/internal/infra"
)

func (s *ActivityService) UpdateActivity(ctx context.Context, activityID int64, title, description *string, sportSectionID, creatorID *int64) (*dto.Activity, error) {
	infra.Infof(ctx, "Updating activity with id=%d", activityID)
	activity, err := s.activityRepository.UpdateActivity(ctx, activityID, title, description, sportSectionID, creatorID)
	if err != nil {
		return nil, fmt.Errorf("cannot update activity with id=%d: %w", activityID, err)
	}

	infra.Infof(ctx, "Getting creator player with id=%v", activity.CreatorID)
	creator, err := s.playerService.GetPlayerByID(ctx, activity.CreatorID)
	if err != nil {
		return nil, fmt.Errorf("cannot get player by id [player_id=%d]: %w", activity.CreatorID, err)
	}

	infra.Infof(ctx, "Activity updated: [activity=%v]", activity)
	return &dto.Activity{Activity: *activity, Creator: *creator}, nil
}
