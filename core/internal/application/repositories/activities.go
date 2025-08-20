package repositories

import (
	"context"
	_ "embed"
	"fmt"
	"match/internal/domain/dao"
	"match/internal/domain/services"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

//go:embed queries/activity/get-by-sport-section-id.sql
var getActivitiesBySportSectionIDQuery string

//go:embed queries/activity/get-by-id.sql
var getActivityByIDQuery string

//go:embed queries/activity/create-activity.sql
var createActivity string

//go:embed queries/activity/delete-activity.sql
var deleteActivity string

//go:embed queries/activity/update-activity.sql
var updateActivity string

type Activities struct {
	pool *pgxpool.Pool
}

func NewActivitiesRepository(pool *pgxpool.Pool) *Activities {
	return &Activities{pool: pool}
}

func (a *Activities) CreateActivity(ctx context.Context, enrollDeadline time.Time, creatorID, sportSectionId int64, title, description string) (*dao.Activity, error) {
	var activity dao.Activity
	err := a.pool.QueryRow(ctx, createActivity, enrollDeadline.String(), title, description, sportSectionId, creatorID).
		Scan(&activity.ID, &activity.EnrollDeadline, &activity.Title, &activity.Description, &activity.SportSectionID, &activity.CreatorID)
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

func (a *Activities) DeleteActivity(ctx context.Context, activityID int64) (*dao.Activity, error) {
	var activity dao.Activity
	err := a.pool.QueryRow(ctx, deleteActivity, activityID).
		Scan(&activity.ID, &activity.Title, &activity.Description, &activity.SportSectionID, &activity.CreatorID)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &activity, nil
}

func (a *Activities) UpdateActivity(ctx context.Context, activityID int64, title, description *string, sportSectionID, creatorID *int64, enrollDeadline time.Time) (*dao.Activity, error) {
	currentActivity, err := a.GetActivityByID(ctx, activityID)
	if err != nil {
		return nil, fmt.Errorf("cannot get activity by id=%d: %w", activityID, err)
	}

	finalTitle := currentActivity.Title
	if title != nil {
		finalTitle = *title
	}

	finalDescription := currentActivity.Description
	if description != nil {
		finalDescription = *description
	}

	finalSportSectionID := currentActivity.SportSectionID
	if sportSectionID != nil {
		finalSportSectionID = *sportSectionID
	}

	finalCreatorID := currentActivity.CreatorID
	if creatorID != nil {
		finalCreatorID = *creatorID
	}

	var activity dao.Activity
	err = a.pool.QueryRow(ctx, updateActivity, activityID, finalTitle, finalDescription, finalSportSectionID, finalCreatorID, enrollDeadline).
		Scan(&activity.ID, &activity.Title, &activity.Description, &activity.SportSectionID, &activity.CreatorID, &enrollDeadline)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &activity, nil
}
