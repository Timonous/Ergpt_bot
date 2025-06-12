package v1

import (
	"github.com/Timonous/Ergpt_bot/webview/pkg/logger"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"net/http"
)

func NewRouter(handler *echo.Echo, l logger.Logger, t IUsersService, n INewsService) {
	// Middleware
	handler.Use(middleware.Logger())
	handler.Use(middleware.Recover())
	//handler.Use(middleware.CORSWithConfig(middleware.CORSConfig{
	//	AllowOrigins:     []string{"http://localhost:3000"},                                                                // Разрешить запросы с этого origin
	//	AllowMethods:     []string{echo.GET, echo.PUT, echo.POST, echo.DELETE, echo.OPTIONS},                               // Разрешенные методы
	//	AllowHeaders:     []string{echo.HeaderOrigin, echo.HeaderContentType, echo.HeaderAccept, echo.HeaderAuthorization}, // Разрешенные заголовки
	//	AllowCredentials: true,                                                                                             // Разрешить передачу кук и заголовков авторизации
	//}))

	handler.GET("/api/article/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})

	h := handler.Group("/api/v1")
	{
		newUserRoutes(h, t, n, l)
	}
}
