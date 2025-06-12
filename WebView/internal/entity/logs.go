package entity

import "time"

type Log struct {
	ID        int       `json:"id"`
	UserID    int       `json:"userID"`
	CommandID int       `json:"commandID"`
	CreatedAt time.Time `json:"createdAt"`
}

type LogWithCommand struct {
	Log
	CommandDescription string `json:"commandDescription"`
}
