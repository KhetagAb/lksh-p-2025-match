package config

import (
	"fmt"
	"match/internal/configs"
	"match/pkg/logger"
	"os"
)

const defaultConfigPath = "configs/config.yaml"

func NewConfig() *configs.Config {
	configPath := os.Getenv("CONFIG_PATH")
	if configPath == "" {
		configPath = defaultConfigPath
	}

	cfg, err := configs.LoadConfig(configPath)
	if err != nil {
		panic(fmt.Sprintf("failed to load configuration: %v", err))
	}
	logger.Init(cfg.App.Name, "info")
	return cfg
}
