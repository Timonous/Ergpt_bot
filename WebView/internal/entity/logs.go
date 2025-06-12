package entity

import "time"

type Log struct {
	ID        int       `json:"id"`
	UserID    int       `json:"userID"`
	CommandID int       `json:"commandID"`
	CreatedAt time.Time `json:"createdAt"`
}

type GetStatisticsRequest struct {
	StartDate time.Time `json:"startDate"`
	EndDate   time.Time `json:"endDate"`
}

type LogsCountByDay struct {
	Day   time.Time `json:"day"`
	Count int       `json:"count"`
}

type GetStatisticsResponse struct {
	GraphInfo          []LogsCountByDay `json:"graphInfo"`
	UniqueUserInPeriod int              `json:"uniqueUserInPeriod"`
}
