package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dao"
	"match/internal/domain/dto"
	"match/internal/infra"
)

func (s *ActivityService) CreateActivity(ctx context.Context, creatorID, sportSectionId int64, title, description string) (*dto.Activity, error) {

	//checking creator by tg_id
	infra.Infof(ctx, "Checking if creator exists: %v", creatorID)
	creator, err := s.playerRepository.GetPlayerByTgID(ctx, creatorID)
	if err != nil {
		infra.Errorf(ctx, "Creator doesn't exist: %v", creatorID)
		return nil, fmt.Errorf("cannot get player by tg_id [player_tg_id=%d]: %w", creatorID, err)
	}

	// Creating activity
	infra.Infof(ctx, "Creating activity: [creatorId=%d][sportSectionId=%d][title=%s][description=%s]", creatorID, sportSectionId, title, description)
	activity, err := s.activityRepository.CreateActivity(ctx, creatorID, sportSectionId, title, description)
	if err != nil {
		infra.Errorf(ctx, "Cannot create activity using given creatorId, sportSectionId, title and description [creatorId=%d][sportSectionId=%d][title=%s][description=%s]",
			creatorID, sportSectionId, title, description)
		return nil, fmt.Errorf("cannot create activity using given creatorId, sportSectionId, title and description [creatorId=%d][sportSectionId=%d][title=%s][description=%s]",
			creatorID, sportSectionId, title, description)
	}

	result := dto.Activity{Activity: dao.Activity{
		ID:             activity.ID,
		Title:          title,
		Description:    description,
		SportSectionID: sportSectionId,
		CreatorID:      creatorID,
	}, Creator: *creator}

	return &result, nil
}
