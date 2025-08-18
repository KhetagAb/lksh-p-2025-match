package mappers

import (
	"match/internal/domain/dto"
	"match/internal/generated/server"
)

func MapTeamToAPI(team dto.Team) server.Team {
	return server.Team{
		Id:      team.Team.ID,
		Name:    team.Team.Name,
		Captain: MapPlayerToAPI(team.Captain),
		Members: server.PlayerList{MapPlayerToAPI(team.Captain)},
	}
}
