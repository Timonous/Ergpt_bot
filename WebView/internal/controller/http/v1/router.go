package v1

import (
	"github.com/Timonous/Ergpt_bot/webview/pkg/logger"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"net/http"
)

type containerRoutes struct {
	t IUsersService
	n INewsService
	s IStatisticsService
	l logger.Logger
}

func newUserRoutes(handler *echo.Group, t IUsersService, n INewsService, s IStatisticsService, l logger.Logger) {
	r := &containerRoutes{t, n, s, l}

	// GET /api/v1/users/{telegramID}
	handler.GET("/users/:telegram_id", r.GetUser)

	// GET /api/v1/news?limit=5&offset=0
	handler.GET("/news", r.GetNews)

	// POST /api/v1/news/like/{news_id}
	handler.POST("/news/like/:news_id", r.LikeNews)

	// POST /api/v1/news/dislike/{news_id}
	handler.POST("/news/dislike/:news_id", r.DislikeNews)

	// GET /api/v1/statistics/graph
	handler.GET("/statistics/graph", r.GetStatisticsGraphic)
}

func NewRouter(handler *echo.Echo, l logger.Logger, t IUsersService, n INewsService, s IStatisticsService) {
	// Middleware
	handler.Use(middleware.Logger())
	handler.Use(middleware.Recover())
	handler.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins:     []string{"http://192.168.0.34:8087"},                                                             // Разрешить запросы с этого origin
		AllowMethods:     []string{echo.GET, echo.PUT, echo.POST, echo.DELETE, echo.OPTIONS},                               // Разрешенные методы
		AllowHeaders:     []string{echo.HeaderOrigin, echo.HeaderContentType, echo.HeaderAccept, echo.HeaderAuthorization}, // Разрешенные заголовки
		AllowCredentials: true,                                                                                             // Разрешить передачу кук и заголовков авторизации
	}))

	handler.GET("/api/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})

	h := handler.Group("/api/v1")
	{
		newUserRoutes(h, t, n, s, l)
	}
}
