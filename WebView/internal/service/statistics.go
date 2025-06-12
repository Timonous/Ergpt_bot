package service

import (
	"context"
	"errors"
	"fmt"
	"github.com/Timonous/Ergpt_bot/webview/internal/entity"
	"time"
)

type ILogsRepository interface {
	GetLogsByDateRange(ctx context.Context, startDate, endDate time.Time) ([]entity.LogWithCommand, error)
	GetNumUsersByPeriod(ctx context.Context, startDate, endDate time.Time) (int, error)
}

type StatisticsService struct {
	logsRepo ILogsRepository
	userRepo IUsersRepository
}

func NewStatisticsService(logsRepo ILogsRepository) *StatisticsService {
	return &StatisticsService{logsRepo: logsRepo}
}

func (s *StatisticsService) GetBotStatistics(ctx context.Context, startDate, endDate time.Time) ([]entity.LogWithCommand, int, error) {
	if startDate.Compare(endDate) != -1 {
		return nil, 0, errors.New("start date must be before end date")
	}

	dateRange, err := s.logsRepo.GetLogsByDateRange(ctx, startDate, endDate)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to get logs by date range: %w", err)
	}

	periodUsers, err := s.logsRepo.GetNumUsersByPeriod(ctx, startDate, endDate)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to get num users by period: %w", err)
	}

	return dateRange, periodUsers, nil
}
