package db

import "github.com/jackc/pgx/v5"

// Create team with only captain
func CreateTeam(conn pgx.Conn, name string, tour_id, captain_id int64) (*int64, error) {
	query := `
		INSERT INTO teams (name, tour_id, captain_id)
		VALUES ($1, $2, $3)
		RETURNING id
    `

	var id int64
	err := conn.QueryRow(ctx, query, name, tour_id, captain_id).Scan(&id)
	if err != nil {
		return nil, &ErrInserting
	}

	// TODO query to add team to players table by captain_id

	return &id, nil
}

func UpdateTeamTourByID(conn pgx.Conn, team_id, tour_id int64) error {
	query := `
		UPDATE teams
		SET tour_id = $2
		WHERE id = $1
	`

	_, err := conn.Exec(ctx, query, team_id, tour_id)
	if err != nil {
		return &ErrUpdating
	}

	return nil
}

func DeleteTeamByID(conn pgx.Conn, id int64) error {
	query := `
		DELETE FROM teams
		WHERE id = $1
	`

	_, err := conn.Exec(ctx, query, id)
	if err != nil {
		return &ErrDeleting
	}

	return nil
}

// TODO DeleteTeamPlayerByID
// TODO AddTeamPlayerByID
