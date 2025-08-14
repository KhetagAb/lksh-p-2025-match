SELECT
    id,
    name,
    captain_id,
    activity_id
FROM teams
WHERE id = $1;
