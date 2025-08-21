package dao

import "time"

type Player struct {
	ID         int64
	Name       string
	TgUsername string
	TgID       int64
}

type SportSection struct {
	ID     int64
	EnName string
	RuName string
}

type Notification struct {
	TelegramID   int64  `mapstructure:"tg_id"`
	MeetingTitle string `mapstructure:"meeting_title"`
}

type Activity struct {
	ID             int64
	Title          string
	Description    string
	SportSectionID int64
	CreatorID      int64
}

type Meeting struct {
	ID         int64
	ActivityID int64
	Title      string
	Date       time.Time
	Details    string
	Status     string
}

type Team struct {
	ID         int64
	Name       string
	CaptainID  int64
	ActivityID int64
}
