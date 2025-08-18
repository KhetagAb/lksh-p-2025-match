package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dao"
	"match/internal/domain/dto"
	"match/internal/infra"
)

func (s *ActivityService) CreateActivity(ctx context.Context, creatorID, sportSectionId int64, title, description string) (*dto.Activity, error) {
	infra.Infof(ctx, "Getting creator player with id=%v", creatorID)
	creator, err := s.playerRepository.GetPlayerByTgID(ctx, creatorID)
	if err != nil {
		infra.Errorf(ctx, "Creator with id=%v doesn't exists or err occured", creatorID)
		return nil, fmt.Errorf("cannot get player by tg_id [player_tg_id=%d]: %w", creatorID, err)
	}
	infra.Infof(ctx, "Getting sport sections with id=%v", sportSectionId)
	sportSections, err := s.sportRepository.GetSportsList(ctx)
	flag := false
	for _, sportSection := range sportSections {
		if sportSection.ID == sportSectionId {
			flag = true
		}
	}
	if !flag {
		infra.Errorf(ctx, "Sport section doesn't exist: %v", sportSectionId)
		return nil, fmt.Errorf("cannot get sport section by id [sport_section_id=%d]: %w", sportSectionId, err)
	}

	if err != nil {
		infra.Errorf(ctx, "Creator doesn't exist: %v", creatorID)
		return nil, fmt.Errorf("cannot get player by tg_id [player_tg_id=%d]: %w", creatorID, err)
	}

	// Checking sports section existence
	infra.Infof(ctx, "Checking if sports section exists: %v", sportSectionId)
	sportSections, err := s.sportRepository.GetAllSportSection(ctx)
	flag := false
	for _, sportSection := range sportSections {
		if sportSection.ID == sportSectionId {
			flag = true
		}
	}
	if !flag {
		infra.Errorf(ctx, "Sport section doesn't exist: %v", sportSectionId)
		return nil, fmt.Errorf("cannot get sport section by id [sport_section_id=%d]: %w", sportSectionId, err)
	}

	// Creating activity
	infra.Infof(ctx, "Creating activity: [creatorId=%d][sportSectionId=%d][title=%s][description=%s]", creatorID, sportSectionId, title, description)
	activity, err := s.activityRepository.CreateActivity(ctx, creatorID, sportSectionId, title, description)
	if err != nil {
		infra.Errorf(ctx, "Cannot create activity using given creatorId, sportSectionId, title and description [creatorId=%d][sportSectionId=%d][title=%s][description=%s]",
			creatorID, sportSectionId, title, description)
		return nil, fmt.Errorf("cannot create activity using given creatorId, sportSectionId, title and description [creatorId=%d][sportSectionId=%d][title=%s][description=%s]: %w",
			creatorID, sportSectionId, title, description, err)
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
