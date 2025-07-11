package service

import (
	"context"
	"github.com/Timonous/Ergpt_bot/webview/internal/entity"
)

type IUsersRepository interface {
	GetUserByTelegramID(ctx context.Context, telegramID string) (*entity.User, error)
	GetUserByUserID(ctx context.Context, userID int) (entity.User, error)
	CheckAuthUser(ctx context.Context, telegramID string) error
}

type UserService struct {
	userRepo IUsersRepository
}

func NewUserService(userRepo IUsersRepository) *UserService {
	return &UserService{userRepo: userRepo}
}

func (s *UserService) GetUserMe(ctx context.Context, telegramID string) (*entity.User, error) {
	return s.userRepo.GetUserByTelegramID(ctx, telegramID)
}

func (s *UserService) IsUserAuth(ctx context.Context, telegramID string) error {
	return s.userRepo.CheckAuthUser(ctx, telegramID)
}
