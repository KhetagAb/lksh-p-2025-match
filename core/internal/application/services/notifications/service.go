package notifications

import (
	"context"
	"errors"
	"time"

	"match/internal/domain/dao"
	"match/internal/domain/services"
)

type (
	NotificationsRepository interface {
		GetCurrentNotifications(ctx context.Context) ([]dao.Notification, error)
		CreateNotification(ctx context.Context, meetingID int64, time time.Time) error
		GetNotificationExistance(ctx context.Context, meetingID int64, time time.Time) bool
		GetExecutedNotifications(ctx context.Context, meetingID int64) ([]dao.Notification, error)
	}

	NotificationsService struct {
		repository NotificationsRepository
	}
)

func NewActivityService(notificationsRepository NotificationsRepository) *NotificationsService {
	return &NotificationsService{repository: notificationsRepository}
}

func (s *NotificationsService) GetCurrentNotifications(ctx context.Context) (services.CurrentNotificationsResponseDTO, error) {
	notifications, err := s.repository.GetCurrentNotifications(ctx)
	var invalidOperationError *services.InvalidOperationError
	if errors.As(err, &invalidOperationError) {
		return services.CurrentNotificationsResponseDTO{}, &services.InvalidOperationError{}
	}

	notifications_ := []services.NotificationDTO{}
	for _, notification := range notifications {
		notifications_ = append(notifications_, services.NotificationDTO{
			TelegramID:   notification.TelegramID,
			MeetingTitle: notification.MeetingTitle,
		})
	}
	return services.CurrentNotificationsResponseDTO{Notifications: notifications_}, nil
}

func (s *NotificationsService) GetExecutedNotifications(ctx context.Context, meetingID int64) (services.ExecutedNotificationsResponseDTO, error) {
	notifications, err := s.repository.GetExecutedNotifications(ctx, meetingID)
	var invalidOperationError *services.InvalidOperationError
	if errors.As(err, &invalidOperationError) {
		return services.ExecutedNotificationsResponseDTO{}, &services.InvalidOperationError{}
	}

	notifications_ := []services.NotificationDTO{}
	for _, notification := range notifications {
		notifications_ = append(notifications_, services.NotificationDTO{
			TelegramID:   notification.TelegramID,
			MeetingTitle: notification.MeetingTitle,
		})
	}
	return services.ExecutedNotificationsResponseDTO{Notifications: notifications_}, nil
}

func (s *NotificationsService) CreateNotification(ctx context.Context, meetingID int64, time time.Time) error {
	exists := s.repository.GetNotificationExistance(ctx, meetingID, time)
	if exists {
		return &services.NotificationAlreadyExists{
			Code:    services.AlreadyExists,
			Message: "Notification already exists",
		}
	}

	err := s.repository.CreateNotification(ctx, meetingID, time)
	if err != nil {
		return err
	}
	return nil
}
