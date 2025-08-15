package infra

import (
	"context"
	"fmt"
	"github.com/jackc/pgx/v5/pgxpool"
)

func NewPgxPool(
	ctx context.Context,
	cfg *Config,
) *pgxpool.Pool {
	db := cfg.Postgres

	connStr := fmt.Sprintf(
		"postgres://%s:%s@%s:%d/%s",
		db.Name,
		db.Password,
		db.Host,
		db.Port,
		db.Database,
	)

	poolConfig, err := pgxpool.ParseConfig(connStr)
	if err != nil {
		panic(fmt.Errorf("unable to parse pool config: %w", err))
	}

	//poolConfig.MaxConns = 10
	//poolConfig.MaxConnLifetime = time.Hour
	//poolConfig.MaxConnIdleTime = 30 * time.Minute

	pool, err := pgxpool.NewWithConfig(ctx, poolConfig)
	if err != nil {
		panic(fmt.Errorf("unable to connect to database: %w", err))
	}

	if err := pool.Ping(ctx); err != nil {
		panic(fmt.Errorf("unable to ping database: %w", err))
	}

	return pool
}
