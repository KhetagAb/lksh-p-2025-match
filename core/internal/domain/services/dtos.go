package services

type (
	NotificationDTO struct {
		TelegramID   int64  `mapstructure:"tg_id"`
		MeetingTitle string `mapstructure:"meeting_id"`
	}
)

type (
	CurrentNotificationsResponseDTO struct {
		Notifications []NotificationDTO
	}

	ExecutedNotificationsResponseDTO struct {
		Notifications []NotificationDTO
	}
)
