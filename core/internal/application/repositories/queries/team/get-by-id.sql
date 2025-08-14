SELECT
    id,
    name,
    captain_id,
    tournament_id
FROM teams
WHERE id = $1;
