package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dto"
	"match/internal/infra"
)

func (s *ActivityService) GetActivitiesBySportSectionID(ctx context.Context, sportSectionID int64) (dto.Activities, error) {
	infra.Infof(ctx, "Getting activities by sport section id [sport_section_id=%d]", sportSectionID)

	activities, err := s.activityRepository.GetActivitiesBySportSectionID(ctx, sportSectionID)
	if err != nil {
		return nil, fmt.Errorf("cannot get list activities by sports section id [sport_section_id=%d]: %w", sportSectionID, err)
	}

	var activitiesDTO dto.Activities
	for _, activity := range activities {
		creator, err := s.playerService.GetPlayerByTgID(ctx, activity.CreatorID)
		if err != nil {
			return nil, fmt.Errorf("cannot get creator of activity by id [activity_id=%d] [activity_title=%s] [activity_creator_id=%d]: %w", activity.ID, activity.Title, activity.CreatorID, err)
		}

		activityDTO := dto.Activity{Activity: activity, Creator: *creator}
		activitiesDTO = append(activitiesDTO, activityDTO)
	}

	infra.Infof(ctx, "Activities by sport section id [sport_section_id=%d] [activities=%v]", sportSectionID, activitiesDTO)
	return activitiesDTO, nil
}
