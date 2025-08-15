package activities

import (
	"context"
	domain "match/internal/domain/dao"
)

type (
	ActivityRepository interface {
		GetActivitiesBySportSectionID(ctx context.Context, sportSectionID int64) ([]domain.Activity, error)
		GetActivityByID(ctx context.Context, id int64) (*domain.Activity, error)
	}

	PlayerRepository interface {
		GetPlayerByID(ctx context.Context, id int64) (*domain.Player, error)
		GetPlayerByTgID(ctx context.Context, tgID int64) (*domain.Player, error)
	}

	TeamRepository interface {
		CreateTeam(ctx context.Context, name string, captainID, activityID int64) (*int64, error)
		AddPlayerToTeam(ctx context.Context, teamID, playerID int64) error
	}

	ActivityService struct {
		activityRepository ActivityRepository
		playerRepository   PlayerRepository
		teamRepository     TeamRepository
	}
)

func NewActivityService(
	activityRepository ActivityRepository,
	playerRepository PlayerRepository,
	teamRepository TeamRepository,
) *ActivityService {
	return &ActivityService{
		activityRepository: activityRepository,
		playerRepository:   playerRepository,
		teamRepository:     teamRepository,
	}
}
