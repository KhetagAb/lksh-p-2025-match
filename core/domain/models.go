package domain

import "time"

type Sport struct {
	ID    int
	Title string
}

type Result struct {
	ID     int
	Result map[int]int
}

type Player struct {
	ID         int
	Name       string
	Username   string
	TelegramID int
}

type Team struct {
	ID        int
	Name      string
	TourID    int
	CaptainID int
}

type Match struct {
	ID       int
	TourID   int
	Teams    []Team
	ResultID int
	SportID  int
}

type Tournament struct {
	ID      int
	SportID int
	Teams   []Team
	Coaches []Player
	Date    time.Time
}
