package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dto"
	"match/internal/infra"
)

func (s *ActivityService) CreateActivity(ctx context.Context, creatorID, sportSectionId int64, title, description string) (*dto.Activity, error) {
	infra.Infof(ctx, "Getting creator player with id=%v", creatorID)
	creator, err := s.playerService.GetPlayerByID(ctx, creatorID)
	if err != nil {
		return nil, fmt.Errorf("cannot get player by tg_id [player_tg_id=%d]: %w", creatorID, err)
	}

	infra.Infof(ctx, "Getting sport sections with id=%v", sportSectionId)
	_, err = s.sportRepository.GetSportSectionByID(ctx, sportSectionId)
	if err != nil {
		return nil, fmt.Errorf("cannot get sport section by id: %w", err)
	}

	infra.Infof(ctx, "Creating activity: [creatorId=%d][sportSectionId=%d][title=%s][description=%s]", creatorID, sportSectionId, title, description)
	activity, err := s.activityRepository.CreateActivity(ctx, creatorID, sportSectionId, title, description)
	if err != nil {
		return nil, fmt.Errorf("cannot create activity with creatorId=%d, sportSectionId=%d, title=%s, description=%s: %w", creatorID, sportSectionId, title, description, err)
	}

	infra.Infof(ctx, "Activity created: [activity=%v]", activity)
	return &dto.Activity{Activity: *activity, Creator: *creator}, nil
}
