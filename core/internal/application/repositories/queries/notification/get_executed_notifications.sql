select players.tg_id, meetings.title
from meeting_participants
inner join meetings on meetings.id = meeting_participants.meeting_id
inner join players on players.id = meeting_participants.player_id
where meeting_participants.meeting_id = $1;
