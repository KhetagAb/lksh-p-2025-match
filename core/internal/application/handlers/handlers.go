package handlers

import (
	"match/internal/presentation"

	"github.com/labstack/echo/v4"
)

type ServerInterface struct {
	registerPlayer              *RegisterPlayerHandler
	getSportList                *GetAllSportSectionHandler
	getTeamsByIDActivity        *GetTeamsByActivityIDHandler
	getActivityBySportSectionID *GetActivitiesBySportSectionIDHandler
	enrollPlayerInActivity      *EnrollPlayerInActivityHandler
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

var _ presentation.ServerInterface = &ServerInterface{}

func NewServerInterface(
	registerPlayer *RegisterPlayerHandler,
	getSportList *GetAllSportSectionHandler,
	getTeamsByIDActivity *GetTeamsByActivityIDHandler,
	getActivityBySportSectionID *GetActivitiesBySportSectionIDHandler,
	enrollPlayerInActivity *EnrollPlayerInActivityHandler,
) *ServerInterface {
	return &ServerInterface{
		getSportList:                getSportList,
		registerPlayer:              registerPlayer,
		getTeamsByIDActivity:        getTeamsByIDActivity,
		getActivityBySportSectionID: getActivityBySportSectionID,
		enrollPlayerInActivity:      enrollPlayerInActivity,
	}
}
