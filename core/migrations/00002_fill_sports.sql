-- +goose Up
INSERT INTO sport_sections (en_name, ru_name)
VALUES ('football', 'футбол'),
       ('volleyball', 'волейбол'),
       ('tennis', 'теннис'),
       ('badminton', 'бадминтон'),
       ('basketball', 'баскетбол'),
       ('pool', 'бильярд'),
       ('shooting', 'стрельба');