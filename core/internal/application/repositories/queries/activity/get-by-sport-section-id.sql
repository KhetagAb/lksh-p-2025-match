SELECT
    id,
    title,
    description,
    sport_section_id,
    creator_id
FROM activities
WHERE sport_section_id = $1;