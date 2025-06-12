package v1

import (
	"context"
	"fmt"
	"github.com/Timonous/Ergpt_bot/webview/internal/entity"
	"github.com/labstack/echo/v4"
	"net/http"
	"strconv"
)

type INewsService interface {
	GetNews(ctx context.Context, limit, offset int) ([]entity.News, error)
	AddLike(ctx context.Context, newsID int) (int, error)
	DeleteLike(ctx context.Context, newsID int) (int, error)
}

func (r *containerRoutes) GetNews(c echo.Context) error {
	ctx := c.Request().Context()

	limitStr := c.QueryParam("limit")
	offsetStr := c.QueryParam("offset")

	// преобразуем limit и offset в числа
	limit, err := strconv.Atoi(limitStr)
	if err != nil || limit < 1 {
		limit = 10 // значение по умолчанию
	}

	offset, err := strconv.Atoi(offsetStr)
	if err != nil || offset < 0 {
		offset = 0 // значение по умолчанию
	}

	news, err := r.n.GetNews(ctx, limit, offset)
	if err != nil {
		errorResponse(c, http.StatusInternalServerError, "internal server error")

		return fmt.Errorf("failed to get news: %w", err)
	}

	return c.JSON(http.StatusOK, entity.PaginatedResponse{
		Items:  news,
		Total:  limit + offset,
		Limit:  limit,
		Offset: offset,
	})
}

func (r *containerRoutes) LikeNews(c echo.Context) error {
	ctx := c.Request().Context()

	newsIDStr := c.Param("news_id")

	newsID, err := strconv.Atoi(newsIDStr)
	if err != nil || newsID < 1 {
		errorResponse(c, http.StatusBadRequest, "wrong news id")

		return fmt.Errorf("failed to get news: %w", err)
	}

	likes, err := r.n.AddLike(ctx, newsID)
	if err != nil {
		errorResponse(c, http.StatusInternalServerError, "failed to add like")

		return fmt.Errorf("failed to add like: %w", err)
	}

	return c.JSON(http.StatusOK, entity.LikeResponse{
		NewsID:   newsID,
		NewLikes: likes,
	})
}

func (r *containerRoutes) DislikeNews(c echo.Context) error {
	ctx := c.Request().Context()

	newsIDStr := c.Param("news_id")

	newsID, err := strconv.Atoi(newsIDStr)
	if err != nil || newsID < 1 {
		errorResponse(c, http.StatusBadRequest, "wrong news id")

		return fmt.Errorf("failed to get news: %w", err)
	}

	likes, err := r.n.DeleteLike(ctx, newsID)
	if err != nil {
		errorResponse(c, http.StatusInternalServerError, "failed to add like")

		return fmt.Errorf("failed to add like: %w", err)
	}

	return c.JSON(http.StatusOK, entity.LikeResponse{
		NewsID:   newsID,
		NewLikes: likes,
	})
}
