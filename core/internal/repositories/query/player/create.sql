INSERT INTO players (name, username, telegram_id)
VALUES ($1, $2, $3)
RETURNING id
