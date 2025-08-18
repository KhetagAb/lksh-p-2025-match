package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dao"
	"match/internal/domain/dto"
)

func (s *ActivityService) CreateActivity(ctx context.Context, creatorID, sportSectionId int64, title, description string) (*dto.Activity, error) {

	//checking creator by tg_id
	creator, err := s.playerRepository.GetPlayerByTgID(ctx, creatorID)
	if err != nil {
		return nil, fmt.Errorf("cannot get player by tg_id [player_tg_id=%d]: %w", creatorID, err)
	}

	// Creating activity
	activity, err := s.activityRepository.CreateActivity(ctx, creatorID, sportSectionId, title, description)
	if err != nil {
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
