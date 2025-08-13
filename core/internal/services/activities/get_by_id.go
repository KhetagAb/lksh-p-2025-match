package activities

import (
	"context"
	"fmt"
	"match/domain"
)

func (s *ActivityService) GetCoreActivityByID(ctx context.Context, tgID, id int64) (*domain.Activity, *domain.Player, error) {
	activity, err := s.activityRepository.GetActivityByID(ctx, id)

	if err != nil {
		return nil, nil, fmt.Errorf("cannot get activity by id [activity_id=%d]: %w", id, err)
	}

	creator, err := s.playerRepository.GetPlayerByTgID(ctx, tgID)
	if err != nil {
		return nil, nil, fmt.Errorf("cannot get creator of activity by id [activity_id=%d] [activity_title=%s] [activity_creator_id=%d]: %w", activity.ID, activity.Title, activity.CreatorID, err)
	}

	return activity, creator, nil
}
