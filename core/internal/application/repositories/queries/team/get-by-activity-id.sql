SELECT
    id,
    name,
    captain_id,
    activity_id
FROM teams
WHERE activity_id = $1;