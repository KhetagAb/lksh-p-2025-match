package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dto"
)

func (s *ActivityService) GetActivitiesBySportSectionID(ctx context.Context, sportSectionID int64) (dto.Activities, error) {
	activities, err := s.activityRepository.GetActivitiesBySportSectionID(ctx, sportSectionID)
	if err != nil {
		return nil, fmt.Errorf("cannot get list activities by sports section id [sport_section_id=%d]: %w", sportSectionID, err)
	}

	var activitiesDTO dto.Activities

	for _, activity := range activities {
		creator, err := s.playerRepository.GetPlayerByID(ctx, activity.CreatorID)
		if err != nil {
			return nil, fmt.Errorf("cannot get creator of activity by id [activity_id=%d] [activity_title=%s] [activity_creator_id=%d]: %w", activity.ID, activity.Title, activity.CreatorID, err)
		}

		activityDTO := dto.Activity{Activity: activity, Creator: *creator}

		activitiesDTO = append(activitiesDTO, activityDTO)
	}

	return activitiesDTO, nil
}
