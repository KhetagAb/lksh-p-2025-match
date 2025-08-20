package repositories

import (
	"context"
	_ "embed"
	"fmt"
	"match/internal/domain/dao"
	"match/internal/domain/services"

	"github.com/jmoiron/sqlx"
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

//go:embed queries/team/add-player-to-team.sql
var addPlayerToTeamQuery string

//go:embed queries/team/get-team-by-player-and-activity.sql
var getTeamByPlayerAndActivityQuery string

//go:embed queries/team/delete-player-from-team-by-activity.sql
var deletePlayerFromTeamByActivity string

type Teams struct {
	db *sqlx.DB
}

func NewTeamsRepository(db *sqlx.DB) *Teams {
	return &Teams{db: db}
}

func (r *Teams) CreateTeam(ctx context.Context, name string, captainID, activityID int64) (*int64, error) {
	var id int64
	err := r.db.QueryRowxContext(ctx, createTeamQuery, name, captainID, activityID).Scan(&id)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	return &id, nil
}

func (r *Teams) GetTeamByID(ctx context.Context, id int64) (*dao.Team, error) {
	var team dao.Team
	err := r.db.GetContext(ctx, &team, getTeamByIDQuery, id)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &team, nil
}

func (r *Teams) GetTeamsByActivityID(ctx context.Context, activityID int64) ([]dao.Team, error) {
	var teams []dao.Team
	err := r.db.SelectContext(ctx, &teams, getTeamsByActivityIDQuery, activityID)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}

	return teams, nil
}

func (r *Teams) GetTeamPlayersByID(ctx context.Context, teamID int64) ([]dao.Player, error) {
	var players []dao.Player
	err := r.db.SelectContext(ctx, &players, getTeamPlayersByIDQuery, teamID)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}

	return players, nil
}

func (r *Teams) DeleteTeamByID(ctx context.Context, id int64) error {
	result, err := r.db.ExecContext(ctx, deleteTeamQuery, id)
	if err != nil {
		return &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}

	if rowsAffected != 1 {
		return &services.NotFoundError{Code: services.NotFound, Message: "team not found"}
	}
	return nil
}

func (r *Teams) AddPlayerToTeam(ctx context.Context, playerID, teamID int64) error {
	_, err := r.db.ExecContext(ctx, addPlayerToTeamQuery, playerID, teamID)
	if err != nil {
		return &services.InvalidOperationError{
			Code:    services.InvalidOperation,
			Message: fmt.Sprintf("failed to add player to team: %v", err),
		}
	}
	return nil
}

func (r *Teams) GetTeamByPlayerAndActivity(ctx context.Context, playerID, activityID int64) (*dao.Team, error) {
	var team dao.Team
	err := r.db.GetContext(ctx, &team, getTeamByPlayerAndActivityQuery, playerID, activityID)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &team, nil
}

func (r *Teams) DeletePlayerFromTeamByActivity(ctx context.Context, playerId, teamId int64) error {
	_, err := r.db.ExecContext(ctx, deletePlayerFromTeamByActivity, playerId, teamId)
	if err != nil {
		return &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}
	return nil
}
