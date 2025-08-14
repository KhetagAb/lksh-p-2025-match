package sport

import (
	"context"
	"match/domain"
)

type (
	GetAllSportSectionService interface {
		GetSportsList(ctx context.Context) ([]domain.SportSection, error)
	}

	SportService struct {
		repository GetAllSportSectionService
	}
)

func (s *SportService) GetAllSportSection(ctx context.Context) ([]domain.SportSection, error) {
	cnt, err := s.repository.GetSportsList(ctx)
	if cnt == nil || err != nil {
		return nil, err
	} else {
		return cnt, nil

	}
}
