package repositories

import (
	"context"
	_ "embed"
	"match/domain"

	"github.com/jackc/pgx/v5/pgxpool"
)

//go:embed queries/team/create.sql
var createTeamQuery string

//go:embed queries/team/get-by-id.sql
var getTeamByIDQuery string

//go:embed queries/team/delete.sql
var deleteTeamQuery string

type Teams struct {
	pool *pgxpool.Pool
}

func NewTeamsRepository(pool *pgxpool.Pool) *Teams {
	return &Teams{pool: pool}
}

func (r *Teams) CreateTeam(
	ctx context.Context,
	name string,
	captainID, tournamentID int32,
) (*int64, error) {
	var id int64
	err := r.pool.QueryRow(ctx, createTeamQuery, name, captainID, tournamentID).Scan(&id)
	if err != nil {
		return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}
	return &id, nil
}

func (r *Teams) GetTeamByID(ctx context.Context, id int32) (*domain.Team, error) {
	var (
		name         string
		captainID    int32
		tournamentID int32
	)

	err := r.pool.QueryRow(ctx, getTeamByIDQuery, id).Scan(&id, &name, &captainID, &tournamentID)
	if err != nil {
		return nil, &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return &domain.Team{
		ID:        id,
		Name:      name,
		CaptainID: captainID,
		TourID:    tournamentID,
	}, nil
}

func (r *Teams) DeleteTeamByID(ctx context.Context, id int32) error {
	tag, err := r.pool.Exec(ctx, deleteTeamQuery, id)
	if err != nil {
		return &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}
	if tag.RowsAffected() != 1 {
		return &domain.NotFoundError{Code: domain.NotFound, Message: "team not found"}
	}
	return nil
}
