package domain

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

const (
	NotFound         = "Not found"
	InvalidOperation = "Invalid operation"
)
