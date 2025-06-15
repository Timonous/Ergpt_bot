package v1

import (
	"context"
	"fmt"
	"github.com/Timonous/Ergpt_bot/webview/internal/entity"
	"github.com/labstack/echo/v4"
	"net/http"
	"strings"
)

type IStatisticsService interface {
	GetBotStatistics(ctx context.Context, startDate, endDate string) ([]entity.LogsCountByDay, int, error)
}

func (r *containerRoutes) GetStatisticsGraphic(c echo.Context) error {
	ctx := c.Request().Context()

	startDate := c.QueryParam("start_date")
	if len(startDate) == 0 {
		errorResponse(c, http.StatusBadRequest, "start_date is required")

		return fmt.Errorf("start_date is required")
	}

	endDate := c.QueryParam("end_date")
	if len(endDate) == 0 {
		errorResponse(c, http.StatusBadRequest, "end_date is required")

		return fmt.Errorf("end_date_date is required")
	}

	statistics, uniqueUsers, err := r.s.GetBotStatistics(ctx, startDate, endDate)
	if err != nil {
		if strings.Contains(err.Error(), "start date must be before end date") {
			errorResponse(c, http.StatusBadRequest, err.Error())

			return fmt.Errorf("failed to get statistics: %w", err)
		}

		errorResponse(c, http.StatusInternalServerError, "internal error")

		return fmt.Errorf("failed to get statistics: %w", err)
	}

	return c.JSON(http.StatusOK, entity.GetStatisticsResponse{
		GraphInfo:          statistics,
		UniqueUserInPeriod: uniqueUsers,
	})
}
