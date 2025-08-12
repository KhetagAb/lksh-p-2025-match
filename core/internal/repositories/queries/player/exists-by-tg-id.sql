SELECT EXISTS (
    SELECT 1
    FROM players
    WHERE tg_id = $1
);
