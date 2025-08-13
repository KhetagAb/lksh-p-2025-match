package activities

import (
	"context"
	"match/domain"
)

type (
	ActivityRepository interface {
		ListActivitiesBySportSectionID(ctx context.Context, sportSectionID int64) ([]domain.Activity, error)
	}

	PlayerRepository interface {
		GetPlayerByID(ctx context.Context, id int64) (*domain.Player, error)
	}

	ActivityService struct {
		activityRepository ActivityRepository
		playerRepository   PlayerRepository
	}
)

func NewActivityService(
	activityRepository ActivityRepository,
	playerRepository PlayerRepository,
) *ActivityService {
	return &ActivityService{
		activityRepository: activityRepository,
		playerRepository:   playerRepository,
	}
}
