package handlers

// вид спорта, начальная и конечная дата, time.data если не указано - текущая дата + неделя
// дедлайн регистрации и название

import (
	"context"
	"errors"
	"github.com/labstack/echo/v4"
	"match/domain"
	"match/internal/generated/server"
	"match/pkg/logger"
)

type (
	CreateTournamentService interface {
		CreateTournament(
			ctx context.Context,
			tournament domain.Tournament,
		) (*int64, error)
	}

	CreateTournamentHandler struct {
		createTournamentService CreateTournamentService
	}
)

func NewCreateTournamentHandler(
	createTournamentService CreateTournamentService,
) *CreateTournamentHandler {
	return &CreateTournamentHandler{
		createTournamentService: createTournamentService,
	}
}

func (h *CreateTournamentHandler) CreateTournament(ectx echo.Context, params server.CreateTournamentParams) error {
	ctx := context.Background()
	logger.Infof(ctx, "Creating a tournament: Name: %v, Sport: %v, Date: %v - %v, RegistrationDealine: %v",
		params.Name, params.Sport, params.StartDate, params.EndDate, params.RegistrationDeadline)
	tournament := domain.Tournament{Name: params.Name, SportSectionID: params.Sport, RegistrationDeadline: params.RegistrationDeadline, StartDate: params.StartDate, EndDate: params.EndDate}
	id, err := h.createTournamentService.CreateTournament(ctx, tournament)
	var tournamentAlreadyExists *domain.TournamentAlreadyExists
	httpCode := 201
	if errors.As(err, &tournamentAlreadyExists) {
		httpCode = 200
	} else if err != nil {
		return InternalErrorResponse(ectx, err.Error())
	}
	return ectx.JSON(httpCode, server.TournamentCreationResponse{Id: id})

}
