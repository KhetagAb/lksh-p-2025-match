INSERT 
INTO sport_sections (en_name, ru_name)
VALUES ($1, $2)
RETURNING id
