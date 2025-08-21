package mappers

import (
	"match/internal/domain/dao"
	"match/internal/domain/dto"
	"match/internal/generated/server"
)

func MapActivityFromAPI(activity server.PostCoreActivityCreateJSONRequestBody) dao.Activity {
	return dao.Activity{
		Title:          activity.Title,
		Description:    activity.Description,
		SportSectionID: activity.SportSectionId,
		CreatorID:      activity.CreatorId,
		EnrollDeadline: activity.EnrollDeadline,
	}
}

func MapActivityToAPI(activity dto.Activity) server.Activity {
	return server.Activity{
		Id:             activity.Activity.ID,
		Creator:        MapPlayerToAPI(activity.Creator),
		Title:          activity.Activity.Title,
		Description:    activity.Activity.Description,
		SportSectionId: activity.Activity.SportSectionID,
	}
}

func MapActivitiesToAPI(activities dto.Activities) []server.Activity {
	resultActivities := []server.Activity{}
	for _, activity := range activities {
		resultActivities = append(resultActivities, MapActivityToAPI(activity))
	}
	return resultActivities
}
