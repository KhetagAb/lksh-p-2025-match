INSERT INTO players (name, tg_username, tg_id)
VALUES ($1, $2, $3)
RETURNING id
