package repositories

import (
	"context"
	_ "embed"
	"match/internal/domain/dao"
	"match/internal/domain/services"

	"github.com/jackc/pgx/v5/pgxpool"
)

//go:embed queries/activity/get-by-sport-section-id.sql
var getActivitiesBySportSectionIDQuery string

//go:embed queries/activity/get-by-id.sql
var getActivityByIDQuery string

//go:embed queries/activity/create-activity.sql
var createActivity string

type Activities struct {
	pool *pgxpool.Pool
}

func NewActivitiesRepository(pool *pgxpool.Pool) *Activities {
	return &Activities{pool: pool}
}

func (a *Activities) CreateActivity(ctx context.Context, creatorID, sportSectionId int64, title, description string) (*dao.Activity, error) {
	var activity dao.Activity
	err := a.pool.QueryRow(ctx, createActivity, title, description, sportSectionId, creatorID).
		Scan(activity.ID, activity.Title, activity.Description, activity.SportSectionID, activity.CreatorID)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	return &activity, nil
}

func (a *Activities) GetActivitiesBySportSectionID(ctx context.Context, sportSectionID int64) ([]dao.Activity, error) {
	rows, err := a.pool.Query(ctx, getActivitiesBySportSectionIDQuery, sportSectionID)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	defer rows.Close()

	activities := make([]dao.Activity, 0)

	for rows.Next() {
		var activity dao.Activity
		if scanErr := rows.Scan(&activity.ID, &activity.Title, &activity.Description, &activity.SportSectionID, &activity.CreatorID); scanErr != nil {
			return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: scanErr.Error()}
		}
		activities = append(activities, activity)
	}

	if rows.Err() != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: rows.Err().Error()}
	}

	return activities, nil
}

func (a *Activities) GetActivityByID(ctx context.Context, id int64) (*dao.Activity, error) {
	var activity dao.Activity
	err := a.pool.QueryRow(ctx, getActivityByIDQuery, id).
		Scan(&activity.ID, &activity.Title, &activity.Description, &activity.SportSectionID, &activity.CreatorID)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &activity, nil
}
