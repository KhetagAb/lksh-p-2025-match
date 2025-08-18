package handlers

import (
	"match/internal/application/handlers/activities"
	"match/internal/application/handlers/players"
	"match/internal/application/handlers/sports"
	"match/internal/application/handlers/teams"
	"match/internal/generated/server"

	"github.com/labstack/echo/v4"
)

type ServerInterface struct {
	registerPlayer              *players.RegisterPlayerHandler
	getSportList                *sports.GetAllSportSectionHandler
	getTeamsByIDActivity        *teams.GetTeamsByActivityIDHandler
	getActivityBySportSectionID *activities.GetActivitiesBySportSectionIDHandler
	enrollPlayerInActivity      *activities.EnrollPlayerInActivityHandler
}

func (s ServerInterface) PostCoreActivityCreate(ctx echo.Context) error {
	//TODO implement me
	panic("implement me")
}

func (s ServerInterface) PostCoreActivityDeleteById(ctx echo.Context, id int64) error {
	//TODO implement me
	panic("implement me")
}

func (s ServerInterface) PostCoreActivityUpdateById(ctx echo.Context, id int64) error {
	//TODO implement me
	panic("implement me")
}

func (s ServerInterface) GetCorePlayerByTg(ctx echo.Context, params server.GetCorePlayerByTgParams) error {
	//TODO implement me
	panic("implement me")
}

func (s ServerInterface) GetCoreTeamsByActivityId(ctx echo.Context, id int64) error {
	return s.getTeamsByIDActivity.GetTeamsByActivityID(ctx, id)
}

func (s ServerInterface) GetCoreActivitiesBySportSectionId(ctx echo.Context, id int64) error {
	return s.getActivityBySportSectionID.GetActivitiesBySportSectionID(ctx, id)
}

func (s ServerInterface) PostCoreActivityIdEnroll(ctx echo.Context, id int64) error {
	return s.enrollPlayerInActivity.EnrollPlayerInActivity(ctx, id)
}

func (s ServerInterface) RegisterPlayer(ctx echo.Context) error {
	return s.registerPlayer.RegisterUser(ctx)
}

func (s ServerInterface) GetCoreSportList(ctx echo.Context) error {
	return s.getSportList.GetAllSportSection(ctx)
}

var _ server.ServerInterface = &ServerInterface{}

func NewServerInterface(
	registerPlayer *players.RegisterPlayerHandler,
	getSportList *sports.GetAllSportSectionHandler,
	getTeamsByIDActivity *teams.GetTeamsByActivityIDHandler,
	getActivityBySportSectionID *activities.GetActivitiesBySportSectionIDHandler,
	enrollPlayerInActivity *activities.EnrollPlayerInActivityHandler,
) *ServerInterface {
	return &ServerInterface{
		getSportList:                getSportList,
		registerPlayer:              registerPlayer,
		getTeamsByIDActivity:        getTeamsByIDActivity,
		getActivityBySportSectionID: getActivityBySportSectionID,
		enrollPlayerInActivity:      enrollPlayerInActivity,
	}
}
