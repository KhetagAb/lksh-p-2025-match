package mappers

import (
	"match/internal/domain/dto"
	"match/internal/generated/server"
)

func MapActivityToAPI(activity dto.Activity) server.Activity {
	description := &activity.Activity.Description
	if *description == "" {
		description = nil
	}
	return server.Activity{
		Id:          activity.Activity.ID,
		Creator:     MapPlayerToAPI(activity.Creator),
		Title:       activity.Activity.Title,
		Description: description,
	}
}

func MapActivitiesToAPI(activities dto.Activities) []server.Activity {
	var resultActivities []server.Activity
	for _, activity := range activities {

		resultActivities = append(resultActivities, MapActivityToAPI(activity))
	}
	return resultActivities
}
