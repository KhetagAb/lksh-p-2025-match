package repositories

import (
	"context"
	_ "embed"
	"match/domain"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

//go:embed queries/tournament/create.sql
var createTournamentQuery string

//go:embed queries/tournament/get-by-id.sql
var getTournamentByIDQuery string

//go:embed queries/tournament/delete.sql
var deleteTournamentQuery string

type Tournaments struct {
	pool *pgxpool.Pool
}

func NewTournamentsRepository(pool *pgxpool.Pool) *Tournaments {
	return &Tournaments{pool: pool}
}

func (t *Tournaments) CreateTournament(
	ctx context.Context,
	name string,
	sportSectionID int64,
	registrationDeadline, startDate, endDate time.Time,
) (*int64, error) {
	var id int64
	err := t.pool.QueryRow(
		ctx,
		createTournamentQuery,
		name,
		sportSectionID,
		registrationDeadline,
		startDate,
		endDate,
	).Scan(&id)

	if err != nil {
		return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}

	return &id, nil
}

func (t *Tournaments) GetTournamentByID(
	ctx context.Context,
	id int64,
) (*domain.Tournament, error) {
	var (
		name           string
		sportSectionID int64
		regDeadline    time.Time
		startDate      time.Time
		endDate        time.Time
	)

	err := t.pool.QueryRow(ctx, getTournamentByIDQuery, id).
		Scan(&id, &name, &sportSectionID, &regDeadline, &startDate, &endDate)
	if err != nil {
		return nil, &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return &domain.Tournament{
		ID:                   id,
		Name:                 name,
		SportSectionID:       sportSectionID,
		RegistrationDeadline: regDeadline,
		StartDate:            startDate,
		EndDate:              endDate,
	}, nil
}

func (t *Tournaments) DeleteTournamentByID(ctx context.Context, id int64) error {
	tag, err := t.pool.Exec(ctx, deleteTournamentQuery, id)
	if err != nil {
		return &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}
	if tag.RowsAffected() != 1 {
		return &domain.NotFoundError{Code: domain.NotFound, Message: "tournament not found"}
	}
	return nil
}
