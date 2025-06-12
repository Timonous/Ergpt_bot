package repository

import (
	"context"
	"fmt"
	"github.com/Timonous/Ergpt_bot/webview/internal/entity"
	"github.com/Timonous/Ergpt_bot/webview/pkg/db/postgres"
)

type NewsRepository struct {
	*postgres.Postgres
}

func NewNewsRepository(pg *postgres.Postgres) *NewsRepository {
	return &NewsRepository{pg}
}

func (n *NewsRepository) GetNews(ctx context.Context, limit, offset uint64) ([]entity.NewsDB, error) {
	sql, args, err := n.Builder.Select(
		"id",
		"header",
		"text",
		"author_id",
		"created_at",
		"likes",
	).
		From("news").
		Limit(limit).
		Offset(offset).
		OrderBy("created_at desc").
		ToSql()
	if err != nil {
		return nil, fmt.Errorf("failed to build query: %w", err)
	}

	rows, err := n.Pool.Query(ctx, sql, args...)
	if err != nil {
		return nil, fmt.Errorf("failed to get news: %w", err)
	}
	defer rows.Close()

	var news []entity.NewsDB
	for rows.Next() {
		var newEnt entity.NewsDB
		err = rows.Scan(&newEnt.ID, &newEnt.Header, &newEnt.Text, &newEnt.AuthorID, &newEnt.CreatedAt, &newEnt.Likes)
		if err != nil {
			return nil, fmt.Errorf("failed to map news: %w", err)
		}

		news = append(news, newEnt)
	}

	return news, nil
}
