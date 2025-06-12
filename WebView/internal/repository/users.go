package repository

import (
	"context"
	"errors"
	"fmt"
	sq "github.com/Masterminds/squirrel"
	"github.com/Timonous/Ergpt_bot/webview/internal/entity"
	"github.com/Timonous/Ergpt_bot/webview/pkg/db/postgres"
	"github.com/jackc/pgx/v4"
)

type UserRepository struct {
	*postgres.Postgres
}

func NewUserRepository(pg *postgres.Postgres) *UserRepository {
	return &UserRepository{pg}
}

func (u *UserRepository) GetUserByTelegramID(ctx context.Context, telegramID string) (*entity.User, error) {
	fmt.Println("GetUserByTelegramID", telegramID)

	query, args, err := u.Builder.Select(
		"u.ID",
		"u.phone",
		"u.telegram_id",
		"u.role_id",
		"u.is_active",
		"s.name",
		"s.surname",
		"s.patronymic",
		"s.is_employed",
		"s.vacancy",
		"s.email",
	).
		From("users u").
		Join("staff s ON u.staff_id = s.id").
		Where(sq.Eq{"u.telegram_id": telegramID}).
		PlaceholderFormat(sq.Dollar).
		ToSql()
	if err != nil {
		return nil, fmt.Errorf("failed to build query: %w", err)
	}

	var user entity.User
	err = u.Pool.QueryRow(context.Background(), query, args...).Scan(
		&user.ID,
		&user.Phone,
		&user.TelegramID,
		&user.RoleID,
		&user.IsActive,
		&user.Name,
		&user.Surname,
		&user.Patronymic,
		&user.IsEmployed,
		&user.Vacancy,
		&user.Email,
	)

	if err != nil {
		if errors.Is(err, pgx.ErrNoRows) {
			return nil, fmt.Errorf("user not found")
		}

		return nil, fmt.Errorf("failed to query user: %w", err)
	}

	return &user, nil
}
