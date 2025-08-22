select players.tg_id, meetings.title
from meeting_participants
inner join meetings on meetings.id = meeting_participants.meeting_id
inner join notifications on notifications.meeting_id = meetings.id
inner join players on players.id = meeting_participants.player_id
where notifications.time_ <= CURRENT_TIMESTAMP;

delete from notifications
where notifications.time_ <= CURRENT_TIMESTAMP;
