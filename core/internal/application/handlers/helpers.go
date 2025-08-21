package handlers

import (
	"fmt"
	"github.com/labstack/echo/v4"
	"match/internal/generated/server"
)

func BadRequestErrorResponsef(ectx echo.Context, message string, a ...any) error {
	return ectx.JSON(400,
		&server.ErrorResponse{
			Message: fmt.Sprintf(message, a...),
		},
	)
}

func InternalErrorResponsef(ectx echo.Context, message string, a ...any) error {
	return ectx.JSON(500,
		&server.ErrorResponse{
			Message: fmt.Sprintf(message, a...),
		},
	)
}

func ConflictErrorResponsef(ectx echo.Context, message string, a ...any) error {
	return ectx.JSON(409,
		&server.ErrorResponse{
			Message: fmt.Sprintf(message, a...),
		},
	)
}

func UnauthorizedErrorResponsef(ectx echo.Context, message string, a ...any) error {
	return ectx.JSON(401, &server.ErrorResponse{
		Message: fmt.Sprintf(message, a...),
	})
}

func NotFoundErrorResponsef(ectx echo.Context, message string, a ...any) error {
	return ectx.JSON(404, &server.ErrorResponse{
		Message: fmt.Sprintf(message, a...),
	})
}

func ForbiddenErrorResponsef(ectx echo.Context, message string, a ...any) error {
	return ectx.JSON(403, &server.ErrorResponse{
		Message: fmt.Sprintf(message, a...),
	})
}
