package handlers

import (
	"context"
	"errors"
	"fmt"
	"match/internal/infra"
	"time"

	"github.com/labstack/echo/v4"

	"match/internal/domain/services"
	"match/internal/generated/server"
)

type (
	NotificationService interface {
		GetCurrentNotifications(ctx context.Context) (services.CurrentNotificationsResponseDTO, error)
		GetExecutedNotifications(ctx context.Context, meetingID int64) (services.ExecutedNotificationsResponseDTO, error)
		CreateNotification(ctx context.Context, meetingID int64, time time.Time) error
	}

	NotificationRouter struct{ service NotificationService }
)

func GetNotificationRouter(service NotificationService) *NotificationRouter {
	return &NotificationRouter{service: service}
}

func validateCreateNotificationRequest(request *server.CreateNotificationRequest) error {
	layout := "2006-01-02 15:04:05"
	_, err := time.Parse(layout, *request.Time)
	if err != nil {
		return fmt.Errorf("time not valid")
	}

	return nil
}

func (s *NotificationRouter) GetCurrentNotifications(ectx echo.Context) error {
	ctx := context.Background()
	response, _ := s.service.GetCurrentNotifications(ctx)

	notifications := []server.Notification{}
	for _, notification := range response.Notifications {
		notifications = append(
			notifications,
			server.Notification{
				MeetingTitle: &notification.MeetingTitle,
				TelegramId:   &notification.TelegramID,
			},
		)
	}

	return ectx.JSON(201, server.CurrentNotificationsResponse{Items: &notifications})
}

func (s *NotificationRouter) GetExecutedNotifications(ectx echo.Context, params server.GetCoreNotificationsParams) error {
	ctx := context.Background()
	response, _ := s.service.GetExecutedNotifications(ctx, params.MeetingId)

	notifications := []server.Notification{}
	for _, notification := range response.Notifications {
		notifications = append(
			notifications,
			server.Notification{
				MeetingTitle: &notification.MeetingTitle,
				TelegramId:   &notification.TelegramID,
			},
		)
	}

	return ectx.JSON(201, server.ExecutedNotificationsResponse{Items: &notifications})
}

func (s *NotificationRouter) CreateNotification(ectx echo.Context) error {
	ctx := context.Background()

	request := new(server.CreateNotificationRequest)

	if err := ectx.Bind(request); err != nil {
		return BadRequestErrorResponsef(ectx, "Invalid request body: %v", err)
	}

	if err := validateCreateNotificationRequest(request); err != nil {
		infra.Errorf(ctx, "Validation error: %v", err)
	}

	layout := "2006-01-02 15:04:05"
	time, _ := time.Parse(layout, *request.Time)
	err := s.service.CreateNotification(ctx, *request.MeetingId, time)

	var invalidOperationError *services.InvalidOperationError
	if errors.As(err, &invalidOperationError) {
		return ConflictErrorResponsef(ectx, "notification already added")
	}
	return ectx.JSON(201, nil)
}
