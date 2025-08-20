DELETE
FROM activities
WHERE id = $1
RETURNING id, title, description, sport_section_id, creator_id;