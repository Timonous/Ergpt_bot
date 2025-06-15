package v1

import (
	"context"
	"fmt"
	"github.com/Timonous/Ergpt_bot/webview/internal/entity"
	"github.com/labstack/echo/v4"
	"net/http"
	"strings"
)

type IUsersService interface {
	GetUserMe(ctx context.Context, telegramID string) (*entity.User, error)
	IsUserAuth(ctx context.Context, telegramID string) error
}

func (r *containerRoutes) GetUser(c echo.Context) error {
	ctx := c.Request().Context()

	telegramID := c.Param("telegram_id")
	if len(telegramID) == 0 {
		c.JSON(http.StatusBadRequest, "telegram_id is required")

		return fmt.Errorf("telegram_id is required")
	}

	user, err := r.t.GetUserMe(ctx, telegramID)
	if err != nil {
		if strings.Contains(err.Error(), "not found") {
			errorResponse(c, http.StatusNotFound, "user not found")

			return fmt.Errorf("user not found")
		}

		errorResponse(c, http.StatusInternalServerError, "failed to get user")

		return fmt.Errorf("failed to get user: %v", err)
	}

	return c.JSON(http.StatusOK, entity.UserResponse{
		ID:            user.ID,
		TelegramID:    user.TelegramID,
		RoleID:        user.RoleID,
		IsActive:      user.IsActive,
		Name:          user.Name,
		Surname:       user.Surname,
		Vacancy:       user.Vacancy,
		Email:         user.Email,
		Phone:         user.Phone,
		PersonalPhone: user.PersonalPhone,
	})
}

func (r *containerRoutes) IsUserAuth(c echo.Context) error {
	ctx := c.Request().Context()

	telegramID := c.Param("telegram_id")
	if len(telegramID) == 0 {
		c.JSON(http.StatusBadRequest, "telegram_id is required")

		return fmt.Errorf("telegram_id is required")
	}

	err := r.t.IsUserAuth(ctx, telegramID)
	if err != nil {
		if strings.Contains(err.Error(), "not found") {
			return c.JSON(http.StatusNotFound, entity.IsUserAuthResponse{
				IsAuth: false,
			})
		}

		errorResponse(c, http.StatusInternalServerError, "failed to get user")

		return fmt.Errorf("failed to get user: %v", err)
	}

	return c.JSON(http.StatusOK, entity.IsUserAuthResponse{
		IsAuth: true,
	})
}
