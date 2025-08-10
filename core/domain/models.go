package domain

import "time"

type Sport struct {
	ID    int64
	Title string
}

type Result struct {
	ID     int64
	Result map[int64]int32
}

type Player struct {
	ID         int64
	Name       string
	Username   string
	TelegramID int64
}

type Team struct {
	ID        int64
	Name      string
	TourID    int64
	CaptainID int64
}

type Match struct {
	ID       int64
	TourID   int64
	Teams    []Team
	ResultID int64
	SportID  int64
}

type Tournament struct {
	ID      int64
	SportID int64
	Teams   []Team
	Coaches []Player
	Date    time.Time
}
