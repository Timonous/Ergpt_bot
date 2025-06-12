package v1

import (
	"context"
	"fmt"
	"github.com/Timonous/Ergpt_bot/webview/internal/entity"
	"github.com/labstack/echo/v4"
	"net/http"
	"time"
)

type IStatisticsService interface {
	GetBotStatistics(ctx context.Context, startDate, endDate time.Time) ([]entity.LogsCountByDay, int, error)
}

func (r *containerRoutes) GetStatisticsGraphic(c echo.Context) error {
	ctx := c.Request().Context()

	u := new(entity.GetStatisticsRequest)
	if err := c.Bind(u); err != nil {
		errorResponse(c, http.StatusBadRequest, "bad request")

		return fmt.Errorf("failed to get request bory: %w", err)
	}

	statistics, uniqurUsers, err := r.s.GetBotStatistics(ctx, u.StartDate, u.EndDate)
	if err != nil {
		errorResponse(c, http.StatusInternalServerError, "internal error")

		return fmt.Errorf("failed to get statistics: %w", err)
	}

	return c.JSON(http.StatusOK, entity.GetStatisticsResponse{
		GraphInfo:          statistics,
		UniqueUserInPeriod: uniqurUsers,
	})
}
