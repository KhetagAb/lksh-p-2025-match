-- +goose Up

create table players
(
    id          bigserial primary key,
    name        varchar(64) not null,
    tg_username varchar(32) not null,
    tg_id       bigint      not null,
    constraint players_tg_id_unique unique (tg_id)
);

create table sport_sections
(
    id      bigserial primary key,
    en_name varchar(64) not null,
    ru_name varchar(64) not null
);

create table activities
(
    id               bigserial primary key,
    title            varchar(64) not null,
    description      text,
    sport_section_id bigint      not null references sport_sections (id),
    creator_id       bigint      not null references players (id),
    enroll_deadline  timestamptz,
    constraint activities_title_unique unique (title)
);

create table teams
(
    id          bigserial primary key,
    name        varchar(64) not null,
    captain_id  bigint      not null references players (id),
    activity_id bigint      not null references activities (id) ON DELETE CASCADE,
    constraint teams_captain_id_activity_id_unique unique (captain_id, activity_id)
);

create table team_players
(
    player_id bigint not null references players (id),
    team_id   bigint not null references teams (id) ON DELETE CASCADE,
    primary key (player_id, team_id)
);

create table meetings
(
    id          bigserial primary key,
    activity_id bigint                   not null references activities (id) ON DELETE CASCADE,
    title       varchar(64)              not null,
    date        timestamp with time zone not null,
    details     text                     not null,
    status      varchar(32)              not null
);

create table meeting_participants
(
    player_id  bigint not null references players (id),
    meeting_id bigint not null references meetings (id) ON DELETE CASCADE
);