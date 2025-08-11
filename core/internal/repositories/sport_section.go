package repositories

import (
	"context"
	_ "embed"
	"match/domain"

	"github.com/jackc/pgx/v5/pgxpool"
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
	pool *pgxpool.Pool
}

func NewSportSectionsRepository(pool *pgxpool.Pool) *SportSections {
	return &SportSections{pool: pool}
}

func (s *SportSections) CreateSportSection(
	ctx context.Context,
	enName, ruName string,
) (*int64, error) {
	var id int64
	if err := s.pool.QueryRow(ctx, createSportSectionQuery, enName, ruName).Scan(&id); err != nil {
		return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}
	return &id, nil
}

func (s *SportSections) GetSportSectionByID(
	ctx context.Context,
	id int32,
) (*domain.SportSection, error) {
	var enName, ruName string
	if err := s.pool.QueryRow(ctx, getSportSectionByIDQuery, id).Scan(&id, &enName, &ruName); err != nil {
		return nil, &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}
	return &domain.SportSection{ID: id, EnName: enName, RuName: ruName}, nil
}

func (s *SportSections) ListSportSections(
	ctx context.Context,
) ([]domain.SportSection, error) {

	rows, err := s.pool.Query(ctx, listSportSectionsQuery)
	if err != nil {
		return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}
	defer rows.Close()

	sections := make([]domain.SportSection, 0)

	for rows.Next() {
		var sec domain.SportSection
		if scanErr := rows.Scan(&sec.ID, &sec.EnName, &sec.RuName); scanErr != nil {
			return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: scanErr.Error()}
		}
		sections = append(sections, sec)
	}

	if rows.Err() != nil {
		return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: rows.Err().Error()}
	}

	return sections, nil
}

func (s *SportSections) DeleteSportSectionByID(ctx context.Context, id int32) error {
	tag, err := s.pool.Exec(ctx, deleteSportSectionQuery, id)
	if err != nil {
		return &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}
	if tag.RowsAffected() != 1 {
		return &domain.NotFoundError{Code: domain.NotFound, Message: "sport section not found"}
	}
	return nil
}
