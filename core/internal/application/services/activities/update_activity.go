package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dto"
	"match/internal/infra"
)

func (s *ActivityService) UpdateActivity(ctx context.Context, activity dto.Activity) (*dto.Activity, error) {
	infra.Infof(ctx, "Updating activity with id=%d", activity.Activity.ID)
	resActivity, err := s.activityRepository.UpdateActivity(ctx, activity.Activity.ID, &activity.Activity.Title, &activity.Activity.Description, &activity.Activity.SportSectionID, &activity.Creator.ID, activity.Activity.EnrollDeadline)

	if err != nil {
		return nil, fmt.Errorf("cannot update activity with id=%d: %w", activity.Activity.ID, err)
	}

	infra.Infof(ctx, "Getting creator player with id=%v", resActivity.CreatorID)
	creator, err := s.playerService.GetPlayerByID(ctx, resActivity.CreatorID)
	if err != nil {
		return nil, fmt.Errorf("cannot get player by id [player_id=%d]: %w", resActivity.CreatorID, err)
	}

	infra.Infof(ctx, "Activity updated: [activity=%v]", activity)
	return &dto.Activity{Activity: *resActivity, Creator: *creator}, nil
}
