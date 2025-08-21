SELECT
    id,
    title,
    description,
    sport_section_id,
    creator_id,
    enroll_deadline
FROM activities
WHERE id = $1;