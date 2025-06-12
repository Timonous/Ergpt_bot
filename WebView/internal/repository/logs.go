package repository

import (
	"context"
	"fmt"
	sq "github.com/Masterminds/squirrel"
	"github.com/Timonous/Ergpt_bot/webview/internal/entity"
	"github.com/Timonous/Ergpt_bot/webview/pkg/db/postgres"
	"time"
)

type LogsRepository struct {
	*postgres.Postgres
}

func NewLogsRepository(pg *postgres.Postgres) *LogsRepository {
	return &LogsRepository{pg}
}

func (l *LogsRepository) GetLogsByDateRange(ctx context.Context, startDate, endDate time.Time) ([]entity.LogWithCommand, error) {
	query, args, err := sq.Select(
		"l.id",
		"l.userID",
		"l.commandID",
		"l.createdAt",
		"c.description as command_description",
	).
		From("logs l").
		Join("commands c ON l.commandID = c.id").
		Where(sq.Expr("l.createdAt BETWEEN ? AND ?", startDate, endDate)).
		OrderBy("l.createdAt DESC").
		ToSql()

	if err != nil {
		return nil, err
	}

	rows, err := l.Pool.Query(ctx, query, args...)
	if err != nil {
		return nil, fmt.Errorf("failed to get logs by date range: %w", err)
	}
	defer rows.Close()

	var logs []entity.LogWithCommand
	for rows.Next() {
		var lg entity.LogWithCommand
		err = rows.Scan(
			&lg.ID,
			&lg.UserID,
			&lg.CommandID,
			&lg.CreatedAt,
			&lg.CommandDescription,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan logs by date range: %w", err)
		}

		logs = append(logs, lg)
	}

	if err = rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to get logs by date range: %w", err)
	}

	return logs, nil
}

func (l *LogsRepository) GetNumUsersByPeriod(ctx context.Context, startDate, endDate time.Time) (int, error) {
	query, args, err := sq.Select("COUNT(DISTINCT userID)").
		From("logs").
		Where(sq.Expr("createdAt BETWEEN ? AND ?", startDate, endDate)).
		PlaceholderFormat(sq.Dollar).
		ToSql()

	if err != nil {
		return 0, fmt.Errorf("failed to build query: %w", err)
	}

	var count int
	err = l.Pool.QueryRow(ctx, query, args...).Scan(&count)
	if err != nil {
		return 0, fmt.Errorf("failed to execute query: %w", err)
	}

	return count, nil
}
