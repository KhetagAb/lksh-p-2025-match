package infra

import (
	"fmt"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq" // PostgreSQL driver
)

func NewSqlxDB(cfg *Config) *sqlx.DB {
	db := cfg.Postgres

	connStr := fmt.Sprintf(
		"postgres://%s:%s@%s:%d/%s?sslmode=disable",
		db.User,
		db.Password,
		db.Host,
		db.Port,
		db.Database,
	)

	sqlxDB, err := sqlx.Connect("postgres", connStr)
	if err != nil {
		panic(fmt.Errorf("unable to connect to database with sqlx: %w", err))
	}

	if err := sqlxDB.Ping(); err != nil {
		panic(fmt.Errorf("unable to ping database with sqlx: %w", err))
	}

	return sqlxDB
}
