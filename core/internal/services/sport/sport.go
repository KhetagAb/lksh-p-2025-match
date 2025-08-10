package handlers

import (
	"context"
	"github.com/labstack/echo/v4"
	"match/internal/repositories"
)

type (
	GetAllSportSectionService interface {
		//TODO возвращать доменный объект
		GetSportsList(ctx context.Context) ([]*repositories.Sport, error)
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
			ans = append(ans, el.Title)

		}
		return ans, nil

	}
}
