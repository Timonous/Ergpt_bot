package service

import (
	"context"
	"fmt"
	"github.com/Timonous/Ergpt_bot/webview/internal/entity"
)

type INewsRepository interface {
	GetNews(ctx context.Context, limit, offset uint64) ([]entity.NewsDB, error)
}

type NewsService struct {
	newsRepo INewsRepository
	userRepo IUsersRepository
}

func NewNewsService(newsRepo INewsRepository, userRepo IUsersRepository) *NewsService {
	return &NewsService{
		newsRepo: newsRepo,
		userRepo: userRepo,
	}
}

func (s *NewsService) GetNews(ctx context.Context, limit, offset int) ([]entity.News, error) {
	news, err := s.newsRepo.GetNews(ctx, uint64(limit), uint64(offset))
	if err != nil {
		return nil, fmt.Errorf("failed to get news: %w", err)
	}

	resNews := make([]entity.News, len(news))
	for _, newEnt := range news {
		user, err := s.userRepo.GetUserByUserID(ctx, newEnt.AuthorID)
		if err != nil {
			return nil, fmt.Errorf("failed to get user by author by id: %w", err)
		}

		resNews = append(resNews, entity.News{
			ID:        newEnt.ID,
			Header:    newEnt.Header,
			Text:      newEnt.Text,
			Author:    user,
			CreatedAt: newEnt.CreatedAt,
			Likes:     newEnt.Likes,
		})
	}

	return resNews, nil
}
