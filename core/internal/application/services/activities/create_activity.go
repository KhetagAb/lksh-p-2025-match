package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dao"
	"match/internal/domain/dto"
	"match/internal/infra"
)

func (s *ActivityService) CreateActivity(ctx context.Context, activity dao.Activity) (*dto.Activity, error) {
	infra.Infof(ctx, "Getting creator player with id=%v", activity.CreatorID)
	creator, err := s.playerService.GetPlayerByID(ctx, activity.CreatorID)
	if err != nil {
		return nil, fmt.Errorf("cannot get player by id [player_id=%d]: %w", activity.CreatorID, err)
	}

	infra.Infof(ctx, "Getting sport sections with id=%v", activity.SportSectionID)
	_, err = s.sportRepository.GetSportSectionByID(ctx, activity.SportSectionID)
	if err != nil {
		return nil, fmt.Errorf("cannot get sport section by id: %w", err)
	}

	infra.Infof(ctx, "Creating activity: [creatorId=%d][sportSectionId=%d][title=%s][description=%v]", activity.CreatorID, activity.SportSectionID, activity.Title, activity.Description)
	resActivity, err := s.activityRepository.CreateActivity(ctx, activity)
	if err != nil {
		return nil, fmt.Errorf("cannot create activity with creatorId=%d, SportSectionID=%d, title=%s, description=%v: %w", activity.CreatorID, activity.SportSectionID, activity.Title, activity.Description, err)
	}

	infra.Infof(ctx, "Activity created: [activity=%v]", activity)
	return &dto.Activity{Activity: *resActivity, Creator: *creator}, nil
}
