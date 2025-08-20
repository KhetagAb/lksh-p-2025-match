package repositories

import (
	"context"
	_ "embed"
	"fmt"
	"match/internal/domain/dao"
	"match/internal/domain/dto"
	"match/internal/domain/services"

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

func (a *Activities) CreateActivity(ctx context.Context, activity dto.Activity) (*dao.Activity, error) {
	var resActivity dao.Activity
	err := a.pool.QueryRow(ctx, createActivity, activity.Activity.EnrollDeadline.String(), activity.Activity.Title, activity.Activity.Description, activity.Activity.SportSectionID, activity.Activity.CreatorID).
		Scan(&resActivity.ID, &resActivity.EnrollDeadline, &resActivity.Title, &resActivity.Description, &resActivity.SportSectionID, &resActivity.CreatorID)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	return &resActivity, nil
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

func (a *Activities) UpdateActivity(ctx context.Context, activity dto.Activity) (*dao.Activity, error) {
	currentActivity, err := a.GetActivityByID(ctx, activity.Activity.ID)
	if err != nil {
		return nil, fmt.Errorf("cannot get activity by id=%d: %w", activity.Activity.ID, err)
	}

	finalTitle := currentActivity.Title
	if activity.Activity.Title != "" {
		finalTitle = activity.Activity.Title
	}

	finalDescription := currentActivity.Description
	if activity.Activity.Description != "" {
		finalDescription = activity.Activity.Description
	}

	finalSportSectionID := currentActivity.SportSectionID
	if activity.Activity.SportSectionID != 0 {
		finalSportSectionID = activity.Activity.SportSectionID
	}

	finalCreatorID := currentActivity.CreatorID
	if activity.Activity.CreatorID != 0 {
		finalCreatorID = activity.Activity.CreatorID
	}

	var resActivity dao.Activity
	err = a.pool.QueryRow(ctx, updateActivity, activity.Activity.ID, finalTitle, finalDescription, finalSportSectionID, finalCreatorID, activity.Activity.EnrollDeadline).
		Scan(&resActivity.ID, &resActivity.Title, &resActivity.Description, &resActivity.SportSectionID, &resActivity.CreatorID, &resActivity.EnrollDeadline)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &resActivity, nil
}
