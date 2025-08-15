SELECT
    id,
    title,
    description,
    sport_section_id,
    creator_id
FROM activities
WHERE id = $1;