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
		DeleteActivity(ctx context.Context, activityID int64) (*dao.Activity, error)
		UpdateActivity(ctx context.Context, activityID int64, title, description *string, sportSectionID, creatorID *int64) (*dao.Activity, error)
	}

	PlayerService interface {
		GetPlayerByID(ctx context.Context, tgId int64) (*dao.Player, error)
	}

	TeamRepository interface {
		CreateTeam(ctx context.Context, name string, captainID, activityID int64) (*int64, error)
		AddPlayerToTeam(ctx context.Context, teamID, playerID int64) error
		GetTeamByPlayerAndActivity(ctx context.Context, playerID, activityID int64) (*dao.Team, error)
		DeletePlayerFromTeamByActivity(ctx context.Context, playerId, teamId int64) error
	}

	SportRepository interface {
		GetSportSectionByID(ctx context.Context, sportSectionID int64) (*dao.SportSection, error)
	}

	ActivityService struct {
		activityRepository ActivityRepository
		playerService      PlayerService
		teamRepository     TeamRepository
		sportRepository    SportRepository
	}
)

func NewActivityService(
	activityRepository ActivityRepository,
	playerService PlayerService,
	teamRepository TeamRepository,
	sportRepository SportRepository,
) *ActivityService {
	return &ActivityService{
		activityRepository: activityRepository,
		playerService:      playerService,
		teamRepository:     teamRepository,
		sportRepository:    sportRepository,
	}
}
