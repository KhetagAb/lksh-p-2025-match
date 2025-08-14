package activities

import (
	"context"
	"fmt"
	"match/internal/domain/dao"
)

func (s *ActivityService) GetActivitiesBySportSectionID(ctx context.Context, sportSectionID int64) ([]dao.Activity, []dao.Player, error) {
	activityList, err := s.activityRepository.GetActivitiesBySportSectionID(ctx, sportSectionID)
	if err != nil {
		return nil, nil, fmt.Errorf("cannot get list activities by sport section id [sport_section_id=%d]: %w", sportSectionID, err)
	}

	var creatorList []dao.Player

	for _, activity := range activityList {
		creator, err := s.playerRepository.GetPlayerByID(ctx, activity.CreatorID)
		if err != nil {
			return nil, nil, fmt.Errorf("cannot get creator of activity by id [activity_id=%d] [activity_title=%s] [activity_creator_id=%d]: %w", activity.ID, activity.Title, activity.CreatorID, err)
		}
		creatorList = append(creatorList, *creator)
	}

	return activityList, creatorList, nil
}
