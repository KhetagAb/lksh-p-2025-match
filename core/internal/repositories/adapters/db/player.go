package db

import "github.com/jackc/pgx/v5"

func CreatePlayer(conn pgx.Conn, username, hashed_password string) (*int64, error) {
	query := `
        INSERT INTO players (username, hashed_password)
        VALUES ($1, $2)
        RETURNING id
    `

	var id int64
	err := conn.QueryRow(ctx, query, username, hashed_password).Scan(&id)
	if err != nil {
		return nil, &ErrInserting
	}

	return &id, nil
}

func GetPlayerIDByUsername(conn pgx.Conn, username string) (*int64, error) {
	query := `
        SELECT id FROM players
		WHERE username = $1
    `

	var id int64
	err := conn.QueryRow(ctx, query, username).Scan(&id)
	if err != nil {
		return nil, &ErrNotFound
	}

	return &id, nil
}

func GetPlayerUsernameByID(conn pgx.Conn, id int64) (*string, error) {
	query := `
        SELECT username FROM players
		WHERE id = $1
    `

	var username string
	err := conn.QueryRow(ctx, query, id).Scan(&username)
	if err != nil {
		return nil, &ErrNotFound
	}

	return &username, nil
}

func GetPlayerHashedPasswordByUsername(conn pgx.Conn, username string) (*string, error) {
	query := `
        SELECT hashed_password FROM players
		WHERE username = $1
    `

	var hashed_password string
	err := conn.QueryRow(ctx, query, username).Scan(&hashed_password)
	if err != nil {
		return nil, &ErrNotFound
	}

	return &hashed_password, nil
}

func GetPlayerHashedPasswordByID(conn pgx.Conn, id int64) (*string, error) {
	query := `
        SELECT hashed_password FROM players
		WHERE id = $1
    `

	var hashed_password string
	err := conn.QueryRow(ctx, query, id).Scan(&hashed_password)
	if err != nil {
		return nil, &ErrNotFound
	}

	return &hashed_password, nil
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

// TODO GetPlayerTeamsByID
// TODO AppendPlayerTeamByID
// TODO RemovePlayerTeamByID
