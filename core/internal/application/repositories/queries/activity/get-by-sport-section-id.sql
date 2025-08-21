SELECT
    id,
    title,
    description,
    sport_section_id,
    creator_id,
    enroll_deadline
FROM activities
WHERE sport_section_id = $1;