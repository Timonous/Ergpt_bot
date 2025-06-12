package main

import (
	"context"
	"fmt"
	"github.com/Timonous/Ergpt_bot/webview/internal/config"
	v1 "github.com/Timonous/Ergpt_bot/webview/internal/controller/http/v1"
	"github.com/Timonous/Ergpt_bot/webview/internal/repository"
	"github.com/Timonous/Ergpt_bot/webview/internal/service"
	"github.com/Timonous/Ergpt_bot/webview/pkg/db/postgres"
	"github.com/Timonous/Ergpt_bot/webview/pkg/httpserver"
	"github.com/Timonous/Ergpt_bot/webview/pkg/logger"
	"github.com/labstack/echo/v4"
	"os"
	"os/signal"
	"strconv"
	"syscall"
)

func main() {
	ctx := context.Background()

	usersLogger := logger.NewLogger()
	ctx = context.WithValue(ctx, logger.LoggerKey, usersLogger)

	cfg := config.MustLoadConfig()
	if cfg == nil {
		panic("load config fail")
	}

	usersLogger.Info(ctx, "read config successfully")

	url := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		cfg.DBConfig.UserName,
		cfg.DBConfig.Password,
		cfg.DBConfig.Host,
		cfg.DBConfig.Port,
		cfg.DBConfig.DbName,
	)

	pg, err := postgres.New(url, postgres.MaxPoolSize(cfg.DBConfig.PoolMax))
	if err != nil {
		usersLogger.Error(ctx, fmt.Sprintf("app - Run - postgres.New: %s", err))
	}
	defer pg.Close()

	usersLogger.Info(ctx, "connected to database successfully")

	userRepo := repository.NewUserRepository(pg)
	newsRepo := repository.NewNewsRepository(pg)

	userService := service.NewUserService(userRepo)
	newsService := service.NewNewsService(newsRepo, userRepo)

	handler := echo.New()

	usersLogger.Info(ctx, fmt.Sprintf("server starting on port:%d", cfg.RestServerPort))

	v1.NewRouter(handler, usersLogger, userService, newsService)

	httpServer := httpserver.New(handler, httpserver.Port(strconv.Itoa(cfg.RestServerPort)))

	// signal for graceful shutdown
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt, syscall.SIGTERM)

	select {
	case s := <-interrupt:
		usersLogger.Info(ctx, "app-Run-signal: "+s.String())
	case err = <-httpServer.Notify():
		usersLogger.Error(ctx, fmt.Sprintf("app-Run-httpServer.Notify: %s", err))
	}

	// shutdown
	err = httpServer.Shutdown()
	if err != nil {
		usersLogger.Error(ctx, fmt.Sprintf("app-Run-httpServer.Shutdown: %s", err))
	}

}
