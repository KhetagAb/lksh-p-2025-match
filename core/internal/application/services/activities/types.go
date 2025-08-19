package activities

import (
	"context"
	"match/internal/domain/dao"
)

type (
	ActivityRepository interface {
		GetActivitiesBySportSectionID(ctx context.Context, sportSectionID int64) ([]dao.Activity, error)
		GetActivityByID(ctx context.Context, id int64) (*dao.Activity, error)
		CreateActivity(ctx context.Context, creatorID, sportSectionId int64, title, description string) (*dao.Activity, error)
	}

	PlayerRepository interface {
		GetPlayerByID(ctx context.Context, id int64) (*dao.Player, error)
		GetPlayerByTgID(ctx context.Context, tgID int64) (*dao.Player, error)
	}

	TeamRepository interface {
		CreateTeam(ctx context.Context, name string, captainID, activityID int64) (*int64, error)
		AddPlayerToTeam(ctx context.Context, teamID, playerID int64) error
		GetTeamByPlayerAndActivity(ctx context.Context, playerID, activityID int64) (*dao.Team, error)
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
