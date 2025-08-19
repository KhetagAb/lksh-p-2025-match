package sports

import (
	"context"
	"match/internal/domain/dao"
)

type (
	SportRepository interface {
		GetSportsList(ctx context.Context) ([]dao.SportSection, error)
	}

	Service struct {
		SportRepository SportRepository
	}
)

func NewSportSectionService(SportRepository SportRepository) *Service {
	return &Service{
		SportRepository: SportRepository,
	}
}

func (s *Service) GetAllSportSection(ctx context.Context) ([]dao.SportSection, error) {
	cnt, err := s.SportRepository.GetSportsList(ctx)
	if cnt == nil || err != nil {
		return nil, err
	} else {
		return cnt, nil

	}
}
