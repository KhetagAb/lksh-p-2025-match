SELECT
    p.id,
    p.name,
    p.tg_username,
    p.tg_id
FROM players p
JOIN team_players tp ON p.id = tp.player_id
WHERE tp.team_id = $1;