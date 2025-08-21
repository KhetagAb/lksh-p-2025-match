package repositories

import (
	"context"
	_ "embed"
	"match/internal/domain/dao"
	"match/internal/domain/services"

	"github.com/jmoiron/sqlx"
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
	db *sqlx.DB
}

func NewActivitiesRepository(db *sqlx.DB) *Activities {
	return &Activities{db: db}
}

func (a *Activities) CreateActivity(ctx context.Context, activity dao.Activity) (*dao.Activity, error) {
	var createdActivity dao.Activity

	var enrollDeadlineStr *string
	if activity.EnrollDeadline != nil {
		str := activity.EnrollDeadline.String()
		enrollDeadlineStr = &str
	}

	err := a.db.QueryRowxContext(ctx, createActivity,
		enrollDeadlineStr,
		activity.Title,
		activity.Description,
		activity.SportSectionID,
		activity.CreatorID).StructScan(&createdActivity)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	return &createdActivity, nil
}

func (a *Activities) GetActivitiesBySportSectionID(ctx context.Context, sportSectionID int64) ([]dao.Activity, error) {
	var activities []dao.Activity

	err := a.db.SelectContext(ctx, &activities, getActivitiesBySportSectionIDQuery, sportSectionID)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}

	return activities, nil
}

func (a *Activities) GetActivityByID(ctx context.Context, id int64) (*dao.Activity, error) {
	var activity dao.Activity
	err := a.db.GetContext(ctx, &activity, getActivityByIDQuery, id)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &activity, nil
}

func (a *Activities) DeleteActivity(ctx context.Context, activityID int64) (*dao.Activity, error) {
	var activity dao.Activity
	err := a.db.QueryRowxContext(ctx, deleteActivity, activityID).StructScan(&activity)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &activity, nil
}

func (a *Activities) UpdateActivity(ctx context.Context, activity dao.Activity) (*dao.Activity, error) {
	var updatedActivity dao.Activity

	var enrollDeadlineStr *string
	if activity.EnrollDeadline != nil {
		str := activity.EnrollDeadline.String()
		enrollDeadlineStr = &str
	}

	err := a.db.QueryRowxContext(ctx, updateActivity,
		activity.ID,
		activity.Title,
		activity.Description,
		activity.SportSectionID,
		activity.CreatorID,
		enrollDeadlineStr).StructScan(&updatedActivity)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &updatedActivity, nil
}
