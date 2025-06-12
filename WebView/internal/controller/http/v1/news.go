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
