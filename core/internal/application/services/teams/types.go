package teams

import (
	"context"
	domain "match/internal/domain/dao"
)

type (
	TeamRepository interface {
		GetTeamsByActivityID(ctx context.Context, activityID int64) ([]domain.Team, error)
		GetTeamPlayersByID(ctx context.Context, teamID int64) ([]domain.Player, error)
	}

	PlayerRepository interface {
		GetPlayerByID(ctx context.Context, id int64) (*domain.Player, error)
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
