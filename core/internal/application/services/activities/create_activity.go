package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dto"
	"match/internal/infra"
)

func (s *ActivityService) CreateActivity(ctx context.Context, activity dto.Activity) (*dto.Activity, error) {
	infra.Infof(ctx, "Getting creator player with id=%v", activity.Creator.ID)
	creator, err := s.playerService.GetPlayerByID(ctx, activity.Creator.ID)
	if err != nil {
		return nil, fmt.Errorf("cannot get player by tg_id [player_tg_id=%d]: %w", activity.Creator.ID, err)
	}

	infra.Infof(ctx, "Getting sport sections with id=%v", activity.Activity.SportSectionID)
	_, err = s.sportRepository.GetSportSectionByID(ctx, activity.Activity.SportSectionID)
	if err != nil {
		return nil, fmt.Errorf("cannot get sport section by id: %w", err)
	}

	infra.Infof(ctx, "Creating activity: [creatorId=%d][SportSectionID=%d][title=%s][description=%s]", activity.Creator.ID, activity.Activity.SportSectionID, activity.Activity.Title, activity.Activity.Description)
	resActivity, err := s.activityRepository.CreateActivity(ctx, activity.Activity.EnrollDeadline, activity.Creator.ID, activity.Activity.SportSectionID, activity.Activity.Title, activity.Activity.Description)
	if err != nil {
		return nil, fmt.Errorf("cannot create activity with creatorId=%d, SportSectionID=%d, title=%s, description=%s: %w", activity.Creator.ID, activity.Activity.SportSectionID, activity.Activity.Title, activity.Activity.Description, err)
	}

	infra.Infof(ctx, "Activity created: [activity=%v]", activity)
	return &dto.Activity{Activity: *resActivity, Creator: *creator}, nil
}
