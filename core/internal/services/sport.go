package handlers

import (
	"context"
	"match/internal/repositories"
)

type (
	GetAllSportSectionService interface {
		//TODO возвращать доменный объект
		GetSportsList(ctx context.Context) ([]*repositories.SportSections, error)
	}

	SportService struct {
		repository GetAllSportSectionService
	}
)

func (s *SportService) GetAllSportSection(ctx context.Context) ([]string, error) {
	cnt, err := s.repository.GetSportsList(ctx)
	if cnt == nil || err != nil {
		return nil, err
	} else {
		var ans []string
		return ans, nil

	}
}
