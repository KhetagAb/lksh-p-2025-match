package handlers

import (
	"github.com/labstack/echo/v4"
	"match/internal/generated/server"
)

func InternalErrorResponse(ectx echo.Context, message string) error {
	return ectx.JSON(500,
		&server.ErrorResponse{
			Message: message,
		},
	)
}

func ConflictErrorResponse(ectx echo.Context, message string) error {
	return ectx.JSON(409,
		&server.ErrorResponse{
			Message: message,
		},
	)
}
