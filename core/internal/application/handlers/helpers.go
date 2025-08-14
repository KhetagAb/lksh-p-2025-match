package handlers

import (
	"github.com/labstack/echo/v4"
	"match/internal/presentation"
)

func InternalErrorResponse(ectx echo.Context, message string) error {
	return ectx.JSON(500,
		&presentation.ErrorResponse{
			Message: message,
		},
	)
}
