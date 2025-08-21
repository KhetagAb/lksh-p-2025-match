package services

import "fmt"

type NotFoundError struct {
	Code    string
	Message string
}

func (e *NotFoundError) Error() string {
	return fmt.Sprintf("Error code %s: %s", e.Code, e.Message)
}

type InvalidOperationError struct {
	Code    string
	Message string
}

func (e *InvalidOperationError) Error() string {
	return fmt.Sprintf("Error code %s: %s", e.Code, e.Message)
}

type NotificationAlreadyExists struct {
	Code    string
	Message string
}

func (e *NotificationAlreadyExists) Error() string {
	return fmt.Sprintf("Error code %s: %s", e.Code, e.Message)
}

type PlayerAlreadyExists struct {
	Code    string
	Message string
}

func (e *PlayerAlreadyExists) Error() string {
	return fmt.Sprintf("Error code %s: %s", e.Code, e.Message)
}

func PlayerAlreadyExistsError(msg string, args ...interface{}) error {
	return &PlayerAlreadyExists{
		Code:    NotFound,
		Message: fmt.Sprintf(msg, args...),
	}
}

type TournamentAlreadyExists struct {
	Code    string
	Message string
}

func (e *TournamentAlreadyExists) Error() string {
	return fmt.Sprintf("Error code %s: %s", e.Code, e.Message)
}

func TournamentAlreadyExistsError(msg string, args ...interface{}) error {
	return &PlayerAlreadyExists{
		Code:    NotFound,
		Message: fmt.Sprintf(msg, args...),
	}
}

const (
	NotFound         = "NOT_FOUND"
	InvalidOperation = "INVALID_OPERATION"
	AlreadyExists    = "ALREADY_EXISTS"
)
