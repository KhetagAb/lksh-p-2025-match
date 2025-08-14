INSERT INTO teams (name, captain_id, activity_id)
VALUES ($1, $2, $3)
RETURNING id;
