package config

import (
	"github.com/Timonous/Ergpt_bot/webview/pkg/db/postgres"
	"github.com/ilyakaznacheev/cleanenv"
)

type Config struct {
	postgres.DBConfig

	RestServerPort int `env:"REST_SERVER_PORT" env-description:"rest server port" env-default:"8080"`
}

func MustLoadConfig() *Config {
	cfg := Config{}
	err := cleanenv.ReadEnv(&cfg)
	if err != nil {
		panic(err)
	}

	return &cfg
}
