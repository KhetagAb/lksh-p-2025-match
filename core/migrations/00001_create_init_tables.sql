-- +goose Up
-- +goose StatementBegin
create table players
(
    id          serial primary key,
    name        varchar(64) not null,
    tg_username varchar(32) not null,
    tg_id       bigint      not null
);

create table sport_sections
(
    id      serial primary key,
    en_name varchar(64) not null,
    ru_name varchar(64) not null
);

create table tournaments
(
    id                    serial primary key,
    name                  varchar(128) not null,
    sport_section_id      int          not null references sport_sections (id),

    registration_deadline date         not null,
    start_date            date         not null,
    end_date              date         not null
);

create table teams
(
    id            serial primary key,
    name          varchar(64) not null,
    captain_id    int         not null references players (id),
    tournament_id int         not null references tournaments (id)
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

-- nothing

-- +goose StatementEnd
