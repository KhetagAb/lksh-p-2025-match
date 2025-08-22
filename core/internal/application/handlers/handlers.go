package handlers

import (
	"match/internal/generated/server"

	"github.com/labstack/echo/v4"
)

type ServerInterface struct {
	registerPlayer              *RegisterPlayerHandler
	getSportList                *GetAllSportSectionHandler
	getTeamsByIDActivity        *GetTeamsByActivityIDHandler
	getActivityBySportSectionID *GetActivitiesBySportSectionIDHandler
	getActivityByID             *GetActivityByIDHandler
	enrollPlayerInActivity      *EnrollPlayerInActivityHandler
	createActivity              *CreateActivityHandler
	deleteActivity              *DeleteActivityHandler
	updateActivity              *UpdateActivityHandler
	getPlayerByTg               *GetPlayerByTgHandler
	deletePlayerFromActivity    *DeletePlayerFromActivityHandler
	notificationRouter          *NotificationRouter
}

func (s ServerInterface) GetCoreNotificationsCurrent(ctx echo.Context) error {
	return s.notificationRouter.GetCurrentNotifications(ctx)
}

func (s ServerInterface) GetCoreNotifications(ctx echo.Context, params server.GetCoreNotificationsParams) error {
	return s.notificationRouter.GetExecutedNotifications(ctx, params)
}

func (s ServerInterface) PostCoreNotifications(ctx echo.Context) error {
	return s.notificationRouter.CreateNotification(ctx)
}

func (s ServerInterface) GetCoreActivityId(ctx echo.Context, id int64) error {
	return s.getActivityByID.GetActivityByID(ctx, id)
}

func (s ServerInterface) PostCoreActivityIdLeave(ctx echo.Context, id int64) error {
	return s.deletePlayerFromActivity.DeletePlayerFromActivity(ctx, id)
}

func (s ServerInterface) PostCoreActivityCreate(ctx echo.Context, params server.PostCoreActivityCreateParams) error {
	return s.createActivity.CreateActivity(ctx, params)
}

func (s ServerInterface) PostCoreActivityDeleteById(ctx echo.Context, id int64, params server.PostCoreActivityDeleteByIdParams) error {
	return s.deleteActivity.DeleteActivity(ctx, id, params)
}

func (s ServerInterface) PostCoreActivityUpdateById(ctx echo.Context, id int64, params server.PostCoreActivityUpdateByIdParams) error {
	return s.updateActivity.UpdateActivity(ctx, id, params)
}

func (s ServerInterface) GetCorePlayerByTg(ctx echo.Context, params server.GetCorePlayerByTgParams) error {
	return s.getPlayerByTg.GetPlayerByTg(ctx, params)
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
	registerPlayer *RegisterPlayerHandler,
	getSportList *GetAllSportSectionHandler,
	getTeamsByIDActivity *GetTeamsByActivityIDHandler,
	getActivityBySportSectionID *GetActivitiesBySportSectionIDHandler,
	getActivityByID *GetActivityByIDHandler,
	enrollPlayerInActivity *EnrollPlayerInActivityHandler,
	createActivity *CreateActivityHandler,
	deleteActivity *DeleteActivityHandler,
	updateActivity *UpdateActivityHandler,
	getPlayerByTg *GetPlayerByTgHandler,
	deletePlayerFromActivity *DeletePlayerFromActivityHandler,
) *ServerInterface {
	return &ServerInterface{
		getSportList:                getSportList,
		registerPlayer:              registerPlayer,
		getTeamsByIDActivity:        getTeamsByIDActivity,
		getActivityBySportSectionID: getActivityBySportSectionID,
		getActivityByID:             getActivityByID,
		enrollPlayerInActivity:      enrollPlayerInActivity,
		createActivity:              createActivity,
		deleteActivity:              deleteActivity,
		updateActivity:              updateActivity,
		getPlayerByTg:               getPlayerByTg,
		deletePlayerFromActivity:    deletePlayerFromActivity,
	}
}
