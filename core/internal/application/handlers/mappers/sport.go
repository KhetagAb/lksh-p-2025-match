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

func MapSportSectionsToAPI(sections []dao.SportSection) []server.SportSection {
	var sportSections []server.SportSection
	for _, section := range sections {
		sportSections = append(sportSections, MapSportToAPI(section))
	}
	return sportSections
}
