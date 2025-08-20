package repositories

import (
	"context"
	_ "embed"
	"match/internal/domain/dao"
	"match/internal/domain/services"

	"github.com/jmoiron/sqlx"
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
	db *sqlx.DB
}

func NewPlayersRepository(db *sqlx.DB) *Players {
	return &Players{db: db}
}

func (p *Players) CreatePlayer(ctx context.Context, name, username string, tgID int64) (*int64, error) {
	var id int64
	err := p.db.QueryRowxContext(ctx, createPlayerQuery, name, username, tgID).Scan(&id)
	if err != nil {
		return nil, &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}

	return &id, nil
}

func (p *Players) GetPlayerByID(ctx context.Context, id int64) (*dao.Player, error) {
	var player dao.Player
	err := p.db.GetContext(ctx, &player, getByIDPlayerQuery, id)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &player, nil
}

func (p *Players) GetPlayerByTgID(ctx context.Context, tgID int64) (*dao.Player, error) {
	var player dao.Player
	err := p.db.GetContext(ctx, &player, getByTgIDPlayerQuery, tgID)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &player, nil
}

func (p *Players) GetPlayerByTgUsername(ctx context.Context, username string) (*dao.Player, error) {
	var player dao.Player
	err := p.db.GetContext(ctx, &player, getByTgUsernamePlayerQuery, username)
	if err != nil {
		return nil, &services.NotFoundError{Code: services.NotFound, Message: err.Error()}
	}

	return &player, nil
}

func (p *Players) GetPlayerExistenceByTgID(ctx context.Context, tgID int64) (bool, error) {
	var exists bool
	err := p.db.QueryRowxContext(ctx, existsByTgIDPlayerQuery, tgID).Scan(&exists)
	if err != nil {
		return false, &services.InvalidOperationError{
			Code:    services.InvalidOperation,
			Message: err.Error(),
		}
	}

	return exists, nil
}

func (p *Players) DeletePlayerByID(ctx context.Context, id int64) error {
	result, err := p.db.ExecContext(ctx, deletePlayerQuery, id)
	if err != nil {
		return &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return &services.InvalidOperationError{Code: services.InvalidOperation, Message: err.Error()}
	}

	if rowsAffected != 1 {
		return &services.NotFoundError{Code: services.NotFound, Message: "player not found"}
	}

	return nil
}
