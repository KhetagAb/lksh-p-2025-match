package mappers

import (
	"match/internal/domain/dao"
	"match/internal/generated/server"
)

func MapSportToAPI(section dao.SportSection) server.SportSection {
	return server.SportSection{
		Id:     section.ID,
		RuName: section.RuName,
		Name:   section.EnName,
	}

}
