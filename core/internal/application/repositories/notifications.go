package repositories

import (
	"context"
	_ "embed"
	"match/internal/domain/dao"
	"match/internal/domain/services"
	"time"

	"github.com/jackc/pgx/v5"

	"github.com/jackc/pgx/v5/pgxpool"
)

var (
	//go:embed queries/notification/get_current_notifications.sql
	getCurrentNotifications string

	//go:embed queries/notification/create_notification.sql
	createNotification string

	//go:embed queries/notification/get_notification_existance.sql
	getNotificationExistance string

	//go:embed queries/notification/get_executed_notifications.sql
	getExecutedNotifications string
)

type NotificationsRepository struct {
	pool *pgxpool.Pool
}

func NewNotificationsRepository(
	pool *pgxpool.Pool,
) *NotificationsRepository {
	return &NotificationsRepository{pool: pool}
}

func (s *NotificationsRepository) GetCurrentNotifications(ctx context.Context) ([]dao.Notification, error) {
	rows, _ := s.pool.Query(ctx, getCurrentNotifications)
	notifications, err := pgx.CollectRows(rows, pgx.RowTo[dao.Notification])
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	return notifications, nil
}

func (s *NotificationsRepository) CreateNotification(ctx context.Context, meetingID int64, time time.Time) error {
	_, err := s.pool.Exec(ctx, createNotification, time, meetingID)
	if err != nil {
		return &services.InvalidOperationError{
			Code:    services.InvalidOperation,
			Message: "Invalid operation",
		}
	}
	return nil
}

func (s *NotificationsRepository) GetNotificationExistance(ctx context.Context, meetingID int64, time time.Time) bool {
	rows, _ := s.pool.Query(ctx, getNotificationExistance, time, meetingID)
	existance, _ := pgx.CollectExactlyOneRow(rows, pgx.RowTo[bool])
	return existance
}

func (s *NotificationsRepository) GetExecutedNotifications(ctx context.Context, meetingID int64) ([]dao.Notification, error) {
	rows, _ := s.pool.Query(ctx, getExecutedNotifications, meetingID)
	notifications, err := pgx.CollectRows(rows, pgx.RowTo[dao.Notification])
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	return notifications, nil
}
