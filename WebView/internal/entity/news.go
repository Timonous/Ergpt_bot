package entity

import "time"

type NewsDB struct {
	ID        int
	Header    string
	Summary   string
	Text      string
	AuthorID  int
	CreatedAt time.Time
	Likes     uint
	Comments  uint
	Category  string
}

type News struct {
	ID        int       `json:"id"`
	Header    string    `json:"title"`
	Summary   string    `json:"summary"`
	Text      string    `json:"content"`
	Author    User      `json:"-"`
	CreatedAt time.Time `json:"date"`
	Likes     uint      `json:"likes"`
	Comments  uint      `json:"comments"`
	Category  string    `json:"category"`
}

type PaginatedResponse struct {
	Items  []News `json:"items"`
	Total  int    `json:"total"`
	Limit  int    `json:"limit"`
	Offset int    `json:"offset"`
}

type LikeResponse struct {
	NewsID   int `json:"news_id"`
	NewLikes int `json:"new_likes"`
}
