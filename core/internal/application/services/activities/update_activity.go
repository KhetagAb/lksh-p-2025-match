package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dto"
	"match/internal/infra"
	"time"
)

func (s *ActivityService) UpdateActivity(ctx context.Context, activityID int64, creatorID *int64, title *string, description *string, enrollDeadline *time.Time) (*dto.Activity, error) {
	infra.Infof(ctx, "Updating activity with id=%d", activityID)

	// Получаем текущую активность
	currentActivity, err := s.activityRepository.GetActivityByID(ctx, activityID)
	if err != nil {
		return nil, fmt.Errorf("cannot get current activity with id=%d: %w", activityID, err)
	}

	// Обновляем только те поля, которые пришли не nil
	updatedActivity := *currentActivity
	if creatorID != nil {
		updatedActivity.CreatorID = *creatorID
	}
	if title != nil {
		updatedActivity.Title = *title
	}
	if description != nil {
		updatedActivity.Description = description
	}
	if enrollDeadline != nil {
		updatedActivity.EnrollDeadline = enrollDeadline
	}

	resActivity, err := s.activityRepository.UpdateActivity(ctx, updatedActivity)
	if err != nil {
		return nil, fmt.Errorf("cannot update activity with id=%d: %w", activityID, err)
	}

	infra.Infof(ctx, "Getting creator player with id=%v", resActivity.CreatorID)
	creator, err := s.playerService.GetPlayerByID(ctx, resActivity.CreatorID)
	if err != nil {
		return nil, fmt.Errorf("cannot get player by id [player_id=%d]: %w", resActivity.CreatorID, err)
	}

	infra.Infof(ctx, "Activity updated: [activity=%v]", updatedActivity)
	return &dto.Activity{Activity: *resActivity, Creator: *creator}, nil
}
