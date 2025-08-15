package teams

import (
	"context"
	"match/internal/domain/dao"
)

type (
	TeamRepository interface {
		GetTeamsByActivityID(ctx context.Context, activityID int64) ([]dao.Team, error)
		GetTeamPlayersByID(ctx context.Context, teamID int64) ([]dao.Player, error)
	}

	PlayerRepository interface {
		GetPlayerByID(ctx context.Context, id int64) (*dao.Player, error)
	}

	TeamService struct {
		teamRepository   TeamRepository
		playerRepository PlayerRepository
	}
)

func NewTeamService(
	teamRepository TeamRepository,
	playerRepository PlayerRepository,
) *TeamService {
	return &TeamService{
		teamRepository:   teamRepository,
		playerRepository: playerRepository,
	}
}
