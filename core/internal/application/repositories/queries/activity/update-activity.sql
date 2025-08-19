UPDATE activities
SET title            = $2,
    description      = $3,
    sport_section_id = $4,
    creator_id       = $5
WHERE id = $1
RETURNING id, title, description, sport_section_id, creator_id;