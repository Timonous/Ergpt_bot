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

func (l *LogsRepository) GetLogsCountByDay(ctx context.Context, startDate, endDate time.Time) ([]entity.LogsCountByDay, error) {
	query, args, err := sq.Select(
		"DATE(l.created_at) as day",
		"COUNT(*) as count",
	).
		From("logs l").
		Where("l.created_at >= $1 AND l.created_at <= $2", startDate, endDate).
		GroupBy("DATE(l.created_at)").
		OrderBy("day ASC").
		ToSql()
	fmt.Println(query, args)
	if err != nil {
		return nil, fmt.Errorf("failed to build query: %w", err)
	}

	rows, err := l.Pool.Query(ctx, query, args...)
	if err != nil {
		return nil, fmt.Errorf("failed to execute query: %w", err)
	}
	defer rows.Close()

	var results []entity.LogsCountByDay
	for rows.Next() {
		var res entity.LogsCountByDay
		err = rows.Scan(
			&res.Day,
			&res.Count,
		)

		if err != nil {
			return nil, fmt.Errorf("failed to scan row: %w", err)
		}

		results = append(results, res)
	}

	return results, nil
}

func (l *LogsRepository) GetNumUsersByPeriod(ctx context.Context, startDate, endDate time.Time) (int, error) {
	query, args, err := sq.Select("COUNT(DISTINCT user_id)").
		From("logs").
		Where(sq.Expr("created_at BETWEEN $1 AND $2", startDate, endDate)).
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
