package db

import (
	"context"

	"github.com/jackc/pgx/v5"
)

var ctx = context.Background()

func CreatePlayer(conn pgx.Conn, name, username string, telegram_id int64) (*int64, error) {
	query := `
        INSERT INTO players (name, username, telegram_id)
        VALUES ($1, $2)
        RETURNING id
    `

	var id int64
	err := conn.QueryRow(ctx, query, name, username, telegram_id).Scan(&id)
	if err != nil {
		return nil, &ErrInserting
	}

	return &id, nil
}

func GetPlayerByID(conn pgx.Conn, id int64) (*Player, error) {
	query := `
		SELECT * FROM players
		WHERE id = $1
	`

	var telegram_id int64
	var name string
	var username string

	err := conn.QueryRow(ctx, query, id).Scan(&id, &name, &username, &telegram_id)
	if err != nil {
		return nil, &ErrNotFound
	}

	return &Player{id, name, username, telegram_id}, nil
}

func DeletePlayerByID(conn pgx.Conn, id int64) error {
	query := `
		DELETE FROM players
		WHERE id = $1
	`

	_, err := conn.Exec(ctx, query, id)
	if err != nil {
		return &ErrDeleting
	}

	return nil
}
