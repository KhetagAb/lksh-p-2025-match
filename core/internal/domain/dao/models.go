package dao

import "time"

type Player struct {
	ID         int64  `db:"id"`
	Name       string `db:"name"`
	TgUsername string `db:"tg_username"`
	TgID       int64  `db:"tg_id"`
}

type SportSection struct {
	ID     int64  `db:"id"`
	EnName string `db:"en_name"`
	RuName string `db:"ru_name"`
}

type Activity struct {
	ID             int64      `db:"id"`
	Title          string     `db:"title"`
	Description    *string    `db:"description"`
	SportSectionID int64      `db:"sport_section_id"`
	CreatorID      int64      `db:"creator_id"`
	EnrollDeadline *time.Time `db:"enroll_deadline"`
}

type Meeting struct {
	ID         int64     `db:"id"`
	ActivityID int64     `db:"activity_id"`
	Title      string    `db:"title"`
	Date       time.Time `db:"date"`
	Details    string    `db:"details"`
	Status     string    `db:"status"`
}

type Team struct {
	ID         int64  `db:"id"`
	Name       string `db:"name"`
	CaptainID  int64  `db:"captain_id"`
	ActivityID int64  `db:"activity_id"`
}
