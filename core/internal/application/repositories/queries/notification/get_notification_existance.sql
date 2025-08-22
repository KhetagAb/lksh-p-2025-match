select exists(
    select notifications.id
    from notifications
    where time_ = $1 and meeting_id = $2
);
