package repositories

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"

	"match/internal/domain"
)

type Sports struct {
	pool *pgxpool.Pool
}

func (s *Sports) CreateSport(ctx context.Context, title string) (*int64, error) {
	query, err := GetQuery("sport", "create")
	if err != nil {
		return nil, &domain.FailedLoadingResourcesError{Code: domain.FailedLoadingResources, Message: err.Error()}
	}

	var id int64
	err = s.pool.QueryRow(ctx, *query, title).Scan(&id)
	if err != nil {
		return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}

	return &id, nil
}

func (s *Sports) GetSportByID(ctx context.Context, id int64) (*Sport, error) {
	query, err := GetQuery("sport", "get-by-id")
	if err != nil {
		return nil, &domain.FailedLoadingResourcesError{Code: domain.FailedLoadingResources, Message: err.Error()}
	}

	var title string
	err = s.pool.QueryRow(ctx, *query, id).Scan(&id, &title)
	if err != nil {
		return nil, &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return &Sport{id, title}, nil

}

func (s *Sports) GetSportsList(ctx context.Context) ([]Sport, error) {
	query, err := GetQuery("sport", "get-list")
	if err != nil {
		return nil, &domain.FailedLoadingResourcesError{Code: domain.FailedLoadingResources, Message: err.Error()}
	}

	rows, err := s.pool.Query(ctx, *query)
	if err != nil {
		return nil, &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}

	defer rows.Close()

	var list []Sport
	var tmp Sport
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
	query, err := GetQuery("sport", "create")
	if err != nil {
		return &domain.FailedLoadingResourcesError{Code: domain.FailedLoadingResources, Message: err.Error()}
	}

	commandTag, err := s.pool.Exec(ctx, *query, id)
	if err != nil {
		return &domain.InvalidOperationError{Code: domain.InvalidOperation, Message: err.Error()}
	}
	if commandTag.RowsAffected() != 1 {
		return &domain.NotFoundError{Code: domain.NotFound, Message: err.Error()}
	}

	return nil
}
