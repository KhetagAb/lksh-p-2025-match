package repositories

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"
)

type Sports struct {
	pool *pgxpool.Pool
}

func (s *Sports) CreateSport(ctx context.Context, title string) (*int64, error) {
	query := `
        INSERT 
		INTO sports (title)
        VALUES ($1)
        RETURNING id
    `

	var id int64
	err := s.pool.QueryRow(ctx, query, title).Scan(&id)
	if err != nil {
		return nil, &ErrInserting
	}

	return &id, nil
}

func (s *Sports) GetSportByID(ctx context.Context, id int64) (*Sport, error) {
	query := `
		SELECT (id, title)
		FROM sports
		WHERE id = $1
	`

	var title string
	err := s.pool.QueryRow(ctx, query, id).Scan(&id, &title)
	if err != nil {
		return nil, &ErrSelecting
	}

	return &Sport{id, title}, nil

}

func (s *Sports) DeleteSportByID(ctx context.Context, id int64) error {
	query := `
		DELETE FROM sports
		WHERE id = $1
	`

	_, err := s.pool.Exec(ctx, query, id)
	if err != nil {
		return &ErrDeleting
	}

	return nil
}
