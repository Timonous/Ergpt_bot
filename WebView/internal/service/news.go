package service

import (
	"context"
	"fmt"
	"github.com/Timonous/Ergpt_bot/webview/internal/entity"
)

const (
	AddLike    = 1
	DeleteLike = -1
)

type INewsRepository interface {
	GetNews(ctx context.Context, limit, offset uint64) ([]entity.NewsDB, error)
	ChangeLike(ctx context.Context, newsID int, vote int) (int, error)
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

	resNews := make([]entity.News, 0)
	for _, newEnt := range news {
		fmt.Println("newEnt", newEnt)
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

func (s *NewsService) AddLike(ctx context.Context, newsID int) (int, error) {
	likes, err := s.newsRepo.ChangeLike(ctx, newsID, AddLike)
	if err != nil {
		return 0, fmt.Errorf("failed to add like: %w", err)
	}

	return likes, nil
}

func (s *NewsService) DeleteLike(ctx context.Context, newsID int) (int, error) {
	likes, err := s.newsRepo.ChangeLike(ctx, newsID, DeleteLike)
	if err != nil {
		return 0, fmt.Errorf("failed to add like: %w", err)
	}

	return likes, nil
}
