package db

import (
	"fmt"
)

type DatabaseError struct {
	Code    int
	Message string
}

func (e *DatabaseError) Error() string {
	return fmt.Sprintf("DatabaseError code %d: %s", e.Code, e.Message)
}

var ErrNotFound = DatabaseError{10, "resource not found"}
var ErrInserting = DatabaseError{11, "failed inserting"}
var ErrUpdating = DatabaseError{12, "failed updating"}
var ErrDeleting = DatabaseError{13, "failed deleting"}
