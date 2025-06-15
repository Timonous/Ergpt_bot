package service

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/Timonous/Ergpt_bot/webview/internal/entity"
)

type ILogsRepository interface {
	GetLogsCountByDay(ctx context.Context, startDate, endDate time.Time) ([]entity.LogsCountByDay, error)
	GetNumUsersByPeriod(ctx context.Context, startDate, endDate time.Time) (int, error)
}

type StatisticsService struct {
	logsRepo ILogsRepository
	userRepo IUsersRepository
}

func NewStatisticsService(logsRepo ILogsRepository) *StatisticsService {
	return &StatisticsService{logsRepo: logsRepo}
}

func (s *StatisticsService) GetBotStatistics(ctx context.Context, startDateStr, endDateStr string) ([]entity.LogsCountByDay, int, error) {
	startDate, err := time.Parse(time.RFC3339, startDateStr)
	fmt.Println(startDate)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to parse start date: %w", err)
	}

	endDate, err := time.Parse(time.RFC3339, endDateStr)
	fmt.Println(endDate)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to parse end date: %w", err)
	}

	if startDate.Compare(endDate) != -1 {
		return nil, 0, errors.New("start date must be before end date")
	}

	dateRange, err := s.logsRepo.GetLogsCountByDay(ctx, startDate, endDate)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to get logs by date range: %w", err)
	}

	periodUsers, err := s.logsRepo.GetNumUsersByPeriod(ctx, startDate, endDate)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to get num users by period: %w", err)
	}

	return dateRange, periodUsers, nil
}
