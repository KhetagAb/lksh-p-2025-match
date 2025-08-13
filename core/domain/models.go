package domain

import (
	"time"
)

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

type Tournament struct {
	ID                   int64
	Name                 string
	SportSectionID       int64
	RegistrationDeadline time.Time
	StartDate            time.Time
	EndDate              time.Time
}

type Team struct {
	ID        int64
	Name      string
	TourID    int64
	CaptainID int64
}
