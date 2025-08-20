package repositories

import (
	"context"
	_ "embed"
	"match/internal/domain/dao"
	"match/internal/domain/services"

	"github.com/jmoiron/sqlx"
)

//go:embed queries/sport_section/create.sql
var createSportSectionQuery string

//go:embed queries/sport_section/get-by-id.sql
var getSportSectionByIDQuery string

//go:embed queries/sport_section/list.sql
var listSportSectionsQuery string

//go:embed queries/sport_section/delete.sql
var deleteSportSectionQuery string

type SportSections struct {
	db *sqlx.DB
}

func NewSportSectionsRepository(db *sqlx.DB) *SportSections {
	return &SportSections{db: db}
}

func (s *SportSections) CreateSportSection(ctx context.Context, enName, ruName string) (*int64, error) {
	var id int64
	if err := s.db.QueryRowxContext(ctx, createSportSectionQuery, enName, ruName).Scan(&id); err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	return &id, nil
}

func (s *SportSections) GetSportSectionByID(ctx context.Context, id int64) (*dao.SportSection, error) {
	var section dao.SportSection
	if err := s.db.GetContext(ctx, &section, getSportSectionByIDQuery, id); err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}
	return &section, nil
}

func (s *SportSections) GetSportsList(ctx context.Context) ([]dao.SportSection, error) {
	var sections []dao.SportSection
	err := s.db.SelectContext(ctx, &sections, listSportSectionsQuery)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}

	return sections, nil
}

func (s *SportSections) DeleteSportSectionByID(ctx context.Context, id int64) error {
	result, err := s.db.ExecContext(ctx, deleteSportSectionQuery, id)
	if err != nil {
		return &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}

	if rowsAffected != 1 {
		return &services.NotFoundError{Code: services.NotFound, Message: "sports section not found"}
	}
	return nil
}
