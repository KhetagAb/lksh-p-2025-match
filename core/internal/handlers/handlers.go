package handlers

import (
	"match/internal/generated/server"

	"github.com/labstack/echo/v4"
)

type ServerInterface struct {
	registerPlayer              *RegisterPlayerHandler
	getTeamsByIDActivity        *GetTeamsByActivityIDHandler
	getActivityBySportSectionID *GetActivityBySportSectionIDHandler
	enrollPlayerInActivity      *EnrollPlayerInActivityHandler
}

func (s ServerInterface) GetCoreTeamsByActivityId(ctx echo.Context, id int64) error {
	return s.getTeamsByIDActivity.GetCoreActivityByID(ctx, id)
}

func (s ServerInterface) GetCoreActivityBySportSectionId(ctx echo.Context, id int64) error {
	return s.getTeamsByIDActivity.GetCoreActivityByID(ctx, id)
}

func (s ServerInterface) PostCoreActivityIdEnroll(ctx echo.Context, id int64) error {
	return s.enrollPlayerInActivity.EnrollPlayerInActivity(ctx, id)
}

func (s ServerInterface) RegisterPlayer(ctx echo.Context) error {
	//TODO implement me
	panic("implement me")
}

func (s ServerInterface) GetCoreSportList(ctx echo.Context) error {
	//TODO implement me
	panic("implement me")
}

var _ server.ServerInterface = &ServerInterface{}

func NewServerInterface(
	registerPlayer *RegisterPlayerHandler,
	getTeamsByIDActivity *GetTeamsByActivityIDHandler,
	getActivityBySportSectionID *GetActivityBySportSectionIDHandler,
	enrollPlayerInActivity *EnrollPlayerInActivityHandler,
) *ServerInterface {
	return &ServerInterface{
		registerPlayer:              registerPlayer,
		getTeamsByIDActivity:        getTeamsByIDActivity,
		getActivityBySportSectionID: getActivityBySportSectionID,
		enrollPlayerInActivity:      enrollPlayerInActivity,
	}
}
