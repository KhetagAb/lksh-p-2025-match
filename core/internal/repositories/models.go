package repositories

import "time"

// table sports
type Sport struct {
	ID    int
	Title string
}

// table results
type Result struct {
	ID       int64
	TeamsIDs []int64
	Results  []int32
}

// table players
type Player struct {
	ID         int64
	Name       string
	Username   string
	TelegramID int64
}

// table teams
type Team struct {
	ID        int64
	Name      string
	TourID    int64
	CaptainID int64
}

// table matches
type Match struct {
	ID       int64
	TourID   int64
	Teams    []Team
	ResultID int64
	SportID  int64
}

// table tournaments
type Tournament struct {
	ID      int64
	SportID int64
	Teams   []Team
	Coaches []Player
	Date    time.Time
}
