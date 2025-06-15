package entity

type User struct {
	ID            int    `json:"id"`
	TelegramID    string `json:"telegram_id"`
	RoleID        int    `json:"role_id"`
	IsActive      bool   `json:"is_active"`
	Name          string `json:"name"`
	Surname       string `json:"surname"`
	Patronymic    string `json:"patronymic"`
	Vacancy       string `json:"vacancy"`
	IsEmployed    bool   `json:"is_employed"`
	Email         string `json:"email"`
	Phone         string `json:"phone"`
	PersonalPhone string `json:"personalPhone"`
}

type UserResponse struct {
	ID            int    `json:"id"`
	TelegramID    string `json:"telegram_id"`
	RoleID        int    `json:"role_id"`
	IsActive      bool   `json:"is_active"`
	Name          string `json:"name"`
	Surname       string `json:"surname"`
	Vacancy       string `json:"position"`
	Email         string `json:"email"`
	Phone         string `json:"workPhone"`
	PersonalPhone string `json:"personalPhone"`
}

type IsUserAuthResponse struct {
	IsAuth bool `json:"is_auth"`
}
