insert into activities (enroll_deadline, title, description, sport_section_id, creator_id)
values (to_timestamp($1, 'YYYY-MM-DD HH24:MI:SS'), $2, $3, $4, $5)
returning id, enroll_deadline, title, description, sport_section_id, creator_id