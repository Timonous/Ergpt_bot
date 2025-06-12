package entity

type Staff struct {
	ID         int    `json:"id"`
	Name       string `json:"name"`
	Surname    string `json:"surname"`
	Patronymic string `json:"patronymic"`
	Vacancy    string `json:"vacancy"`
	IsEmployed bool   `json:"is_employed"`
	Email      string `json:"email"`
	Phone      string `json:"phone"`
}
