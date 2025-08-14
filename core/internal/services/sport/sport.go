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

func (s *SportService) GetAllSportSection(ctx context.Context) ([]string, error) {
	cnt, err := s.repository.GetSportsList(ctx)
	if cnt == nil || err != nil {
		return nil, err
	} else {
		var ans []string
		for _, el := range cnt {
			ans = append(ans, el.RuName)
		}
		return ans, nil

	}
}
