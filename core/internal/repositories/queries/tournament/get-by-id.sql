SELECT
    id,
    name,
    sport_section_id,
    registration_deadline,
    start_date,
    end_date
FROM tournaments
WHERE id = $1;
