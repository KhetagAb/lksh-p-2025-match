INSERT INTO tournaments (
    name,
    sport_section_id,
    registration_deadline,
    start_date,
    end_date
) VALUES ($1, $2, $3, $4, $5)
RETURNING id;
