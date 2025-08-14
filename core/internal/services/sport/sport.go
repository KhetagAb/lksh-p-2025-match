package sport

import (
	"context"
	"match/domain"
)

type (
	Repository interface {
		GetSportsList(ctx context.Context) ([]domain.SportSection, error)
	}

	Service struct {
		repository Repository
	}
)

func NewSportSectionService(repository Repository) *Service {
	return &Service{
		repository: repository,
	}
}

func (s *Service) GetAllSportSection(ctx context.Context) ([]domain.SportSection, error) {
	cnt, err := s.repository.GetSportsList(ctx)
	if cnt == nil || err != nil {
		return nil, err
	} else {
		return cnt, nil

	}
}
