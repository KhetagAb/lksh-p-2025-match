package repositories

import (
	"context"
	_ "embed"
	"match/internal/domain/dao"
	"match/internal/domain/services"

	"github.com/jackc/pgx/v5/pgxpool"
)

var (
	//go:embed queries/player/create.sql
	createPlayerQuery string

	//go:embed queries/player/get-by-id.sql
	getByIDPlayerQuery string

	//go:embed queries/player/get-by-tg-id.sql
	getByTgIDPlayerQuery string

	//go:embed queries/player/get-by-tg-username.sql
	getByTgUsernamePlayerQuery string

	//go:embed queries/player/exists-by-tg-id.sql
	existsByTgIDPlayerQuery string

	//go:embed queries/player/delete.sql
	deletePlayerQuery string
)

type Players struct {
	pool *pgxpool.Pool
}

func NewPlayersRepository(
	pool *pgxpool.Pool,
) *Players {
	return &Players{pool: pool}
}

func (p *Players) CreatePlayer(ctx context.Context, name, username string, tgID int64) (*int64, error) {
	var id int64
	err := p.pool.QueryRow(ctx, createPlayerQuery, name, username, tgID).Scan(&id)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}

	return &id, nil
}

func (p *Players) GetPlayerByID(ctx context.Context, id int64) (*dao.Player, error) {
	var tgID int64
	var name string
	var username string

	err := p.pool.QueryRow(ctx, getByIDPlayerQuery, id).Scan(&id, &name, &username, &tgID)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &dao.Player{ID: id, Name: name, TgUsername: username, TgID: tgID}, nil
}

func (p *Players) GetPlayerByTgID(ctx context.Context, tgID int64) (*dao.Player, error) {
	var id int64
	var name string
	var username string

	err := p.pool.QueryRow(ctx, getByTgIDPlayerQuery, tgID).Scan(&id, &name, &username, &tgID)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &dao.Player{ID: id, Name: name, TgUsername: username, TgID: tgID}, nil
}

func (p *Players) GetPlayerByTgUsername(ctx context.Context, username string) (*dao.Player, error) {
	var id int64
	var name string
	var tgID int64

	err := p.pool.QueryRow(ctx, getByTgUsernamePlayerQuery, username).Scan(&id, &name, &username, &tgID)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &dao.Player{ID: id, Name: name, TgUsername: username, TgID: tgID}, nil
}

func (p *Players) GetPlayerExistenceByTgID(
	ctx context.Context,
	tgID int64,
) (bool, error) {

	var exists bool
	err := p.pool.QueryRow(ctx, existsByTgIDPlayerQuery, tgID).Scan(&exists)
	if err != nil {
		return false, &services.InvalidOperationError{
			Code:    services.InvalidOperation,
			Message: err.Error(),
		}
	}

	return exists, nil
}

func (p *Players) DeletePlayerByID(ctx context.Context, id int64) error {
	commandTag, err := p.pool.Exec(ctx, deletePlayerQuery, id)
	if err != nil {
		return &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}
	if commandTag.RowsAffected() != 1 {
		return &services.NotFoundError{Code: services.NotFound, Message: "player not found"}
	}

	return nil
}
