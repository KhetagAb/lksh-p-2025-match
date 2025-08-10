package repositories

import (
	"context"
	_ "embed"

	"github.com/jackc/pgx/v5/pgxpool"

	"match/domain"
)

var (
	//go:embed queries/sport/create.sql
	createSportQuery string

	//go:embed queries/player/get-by-id.sql
	getByIDSportQuery string

	//go:embed queries/player/get-by-telegram-id.sql
	getSportsListQuery string

	//go:embed queries/player/delete.sql
	deleteSportQuery string
)

type Sports struct {
	pool *pgxpool.Pool
}

func (s *Sports) CreateSport(ctx context.Context, title string) (*int64, error) {
	var id int64
	err := s.pool.QueryRow(ctx, createSportQuery, title).Scan(&id)
	if err != nil {
		return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}

	return &id, nil
}

func (s *Sports) GetSportByID(ctx context.Context, id int64) (*domain.Sport, error) {
	var title string
	err := s.pool.QueryRow(ctx, getByIDSportQuery, id).Scan(&id, &title)
	if err != nil {
		return nil, &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return &domain.Sport{ID: id, Title: title}, nil

}

func (s *Sports) GetSportsList(ctx context.Context) ([]domain.Sport, error) {
	rows, err := s.pool.Query(ctx, getSportsListQuery)
	if err != nil {
		return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}

	defer rows.Close()

	var list []domain.Sport
	var tmp domain.Sport
	for rows.Next() {
		err := rows.Scan(&tmp.ID, &tmp.Title)
		if err != nil {
			return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
		}
		list = append(list, tmp)
	}

	return list, nil

}

func (s *Sports) DeleteSportByID(ctx context.Context, id int64) error {
	commandTag, err := s.pool.Exec(ctx, deleteSportQuery, id)
	if err != nil {
		return &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}
	if commandTag.RowsAffected() != 1 {
		return &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return nil
}
