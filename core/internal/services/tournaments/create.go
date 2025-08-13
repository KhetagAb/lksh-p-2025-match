package tournaments

import (
	"context"
	"errors"
	"fmt"
	"match/domain"
)

type (
	TournamentRepository interface {
		CreateTournament(
			ctx context.Context,
			tournament domain.Tournament,
		) (*int64, error)
	}

	TournamentService struct {
		repository TournamentRepository
	}
)

func NewTournamentService(
	repository TournamentRepository,
) *TournamentService {
	return &TournamentService{
		repository: repository,
	}
}

func (s *TournamentService) CreateTournament(ctx context.Context, tournament domain.Tournament) (*int64, error) {
	id, err := s.repository.CreateTournament(ctx, tournament)

	var notFoundError *domain.NotFoundError
	var tournamentAlreadyExists *domain.TournamentAlreadyExists
	var null int64
	if errors.As(err, &notFoundError) {
		return &null, nil
	}
	if errors.As(err, &tournamentAlreadyExists) {
		return &null, fmt.Errorf("tournament ( Name: %v, Sport: %v, Date: %v - %v, RegistrationDealine: %v) already exists: %w",
			tournament.Name, tournament.SportSectionID, tournament.StartDate, tournament.EndDate, tournament.RegistrationDeadline, err)
	}
	if err != nil {
		return &null, fmt.Errorf("cannot create tournament: Name: %v, Sport: %v, Date: %v - %v, RegistrationDealine: %v: %w",
			tournament.Name, tournament.SportSectionID, tournament.StartDate, tournament.EndDate, tournament.RegistrationDeadline, err)
	}

	return id, nil
}
