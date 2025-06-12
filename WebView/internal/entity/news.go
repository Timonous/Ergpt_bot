package entity

import "time"

type NewsDB struct {
	ID        int
	Header    string
	Text      string
	AuthorID  int
	CreatedAt time.Time
	Likes     uint
}

type News struct {
	ID        int
	Header    string
	Text      string
	Author    User
	CreatedAt time.Time
	Likes     uint
}

type PaginatedResponse struct {
	Items  []News `json:"items"`
	Total  int    `json:"total"`
	Limit  int    `json:"limit"`
	Offset int    `json:"offset"`
}
