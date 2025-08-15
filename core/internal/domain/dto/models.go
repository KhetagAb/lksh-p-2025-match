package dto

import "match/internal/domain/dao"

type Team struct {
	team    dao.Team
	captain dao.Player
	players []dao.Player
}
type Teams = []Team

type Activity struct {
	activity dao.Activity
	creator  dao.Player
}
type Activities = []Activity
