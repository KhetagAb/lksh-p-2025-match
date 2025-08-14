package repositories

import (
	"context"
	_ "embed"
	domain "match/internal/domain/dao"
	"match/internal/domain/services"

	"github.com/jackc/pgx/v5/pgxpool"
)

//go:embed queries/team/create.sql
var createTeamQuery string

//go:embed queries/team/get-by-id.sql
var getTeamByIDQuery string

//go:embed queries/team/delete.sql
var deleteTeamQuery string

//go:embed queries/team/get-by-activity-id.sql
var getTeamsByActivityIDQuery string

//go:embed queries/team/get-players-by-team-id.sql
var getTeamPlayersByIDQuery string

type Teams struct {
	pool *pgxpool.Pool
}

func NewTeamsRepository(pool *pgxpool.Pool) *Teams {
	return &Teams{pool: pool}
}

func (r *Teams) CreateTeam(
	ctx context.Context,
	name string,
	captainID, activityID int64,
) (*int64, error) {
	var id int64
	err := r.pool.QueryRow(ctx, createTeamQuery, name, captainID, activityID).Scan(&id)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	return &id, nil
}

func (r *Teams) GetTeamByID(ctx context.Context, id int64) (*domain.Team, error) {
	var (
		name       string
		captainID  int64
		activityID int64
	)

	err := r.pool.QueryRow(ctx, getTeamByIDQuery, id).Scan(&id, &name, &captainID, &activityID)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &domain.Team{
		ID:         id,
		Name:       name,
		CaptainID:  captainID,
		ActivityID: activityID,
	}, nil
}

func (r *Teams) GetTeamsByActivityID(ctx context.Context, activityID int64) ([]domain.Team, error) {
	rows, err := r.pool.Query(ctx, getTeamsByActivityIDQuery, activityID)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	defer rows.Close()

	teams := make([]domain.Team, 0)

	for rows.Next() {
		var team domain.Team
		if scanErr := rows.Scan(&team.ID, &team.Name, &team.CaptainID, &team.ActivityID); scanErr != nil {
			return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: scanErr.Error()}
		}
		teams = append(teams, team)
	}

	if rows.Err() != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: rows.Err().Error()}
	}

	return teams, nil
}

func (r *Teams) GetTeamPlayersByID(ctx context.Context, teamID int64) ([]domain.Player, error) {
	rows, err := r.pool.Query(ctx, getTeamPlayersByIDQuery, teamID)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	defer rows.Close()

	players := make([]domain.Player, 0)

	for rows.Next() {
		var player domain.Player
		if scanErr := rows.Scan(&player.ID, &player.Name, &player.TgUsername, &player.TgID); scanErr != nil {
			return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: scanErr.Error()}
		}
		players = append(players, player)
	}

	if rows.Err() != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: rows.Err().Error()}
	}

	return players, nil
}

func (r *Teams) DeleteTeamByID(ctx context.Context, id int64) error {
	tag, err := r.pool.Exec(ctx, deleteTeamQuery, id)
	if err != nil {
		return &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	if tag.RowsAffected() != 1 {
		return &services.NotFoundError{Code: services.NotFound, Message: "team not found"}
	}
	return nil
}
