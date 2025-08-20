insert into activities (title, description, sport_section_id, creator_id)
values ($1, $2, $3, $4)
returning id, title, description, sport_section_id, creator_id