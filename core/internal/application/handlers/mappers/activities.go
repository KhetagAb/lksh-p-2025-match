package mappers

import (
	"match/internal/domain/dto"
	"match/internal/generated/server"
)

func MapActivityToAPI(activity dto.Activity) server.Activity {
	return server.Activity{
		Id:          activity.Activity.ID,
		Creator:     MapPlayerToAPI(activity.Creator),
		Title:       activity.Activity.Title,
		Description: &activity.Activity.Description,
	}
}
