package dto

import "match/internal/domain/dao"

type Team struct {
	Team    dao.Team
	Captain dao.Player
	Players []dao.Player
}
type Teams = []Team

type Activity struct {
	Activity dao.Activity
	Creator  dao.Player
}
type Activities = []Activity
