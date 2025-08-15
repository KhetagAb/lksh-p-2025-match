SELECT
    t.id,
    t.name,
    t.captain_id,
    t.activity_id
FROM teams t
JOIN team_players tp ON t.id = tp.team_id
WHERE tp.player_id = $1 AND t.activity_id = $2;