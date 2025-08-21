-- +goose Up

create table notifications (
    id         bigserial                primary key,
    time       timestamp with time zone not null,
    meeting_id bigint                   not null references meetings(id),
);
