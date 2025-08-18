package mappers

import (
	"match/internal/domain/dao"
	"match/internal/generated/server"
)

func MapPlayerToAPI(player dao.Player) server.Player {
	return server.Player{
		Name:       player.Name,
		TgUsername: player.TgUsername,
		CoreId:     player.ID,
		TgId:       player.TgID,
	}
}

func MapDAOPlayerListToServerPlayerList(players []dao.Player) []server.Player {
	var serverPlayers []server.Player
	for _, p := range players {
		serverPlayers = append(serverPlayers, MapPlayerToAPI(p))

	}
	return serverPlayers
}
