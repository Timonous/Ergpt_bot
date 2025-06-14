package repository

import (
	"context"
	"fmt"
	sq "github.com/Masterminds/squirrel"
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
		"summary",
		"comments",
		"category",
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
		err = rows.Scan(
			&newEnt.ID,
			&newEnt.Header,
			&newEnt.Text,
			&newEnt.AuthorID,
			&newEnt.CreatedAt,
			&newEnt.Likes,
			&newEnt.Summary,
			&newEnt.Comments,
			&newEnt.Category,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to map news: %w", err)
		}

		news = append(news, newEnt)
	}

	return news, nil
}

func (n *NewsRepository) ChangeLike(ctx context.Context, newsID int, vote int) (int, error) {
	sql, args, err := n.Builder.Update("news").
		Set("likes", sq.Expr(fmt.Sprintf("%s + %d", "likes", vote))).
		Where(sq.Eq{"id": newsID}).
		Suffix("RETURNING likes").
		ToSql()

	var newValueLikes int
	err = n.Pool.QueryRow(ctx, sql, args...).Scan(&newValueLikes)
	if err != nil {
		return 0, fmt.Errorf("failed to add like: %w", err)
	}

	return newValueLikes, nil
}
