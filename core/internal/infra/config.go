package infra

import (
	"context"
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/joho/godotenv"
	"github.com/spf13/viper"
)

func NewContextProvider() context.Context {
	return context.Background()
}

type (
	Config struct {
		App      AppConfig      `mapstructure:"app"`
		HTTP     HTTPConfig     `mapstructure:"http"`
		Postgres PostgresConfig `mapstructure:"postgres"`
	}

	PostgresConfig struct {
		Host     string `mapstructure:"host"`
		User     string `mapstructure:"user"`
		Password string `mapstructure:"password"`
		Database string `mapstructure:"database"`
		Port     int    `mapstructure:"port"`
	}

	AppConfig struct {
		Name    string `mapstructure:"name"`
		Version string `mapstructure:"version"`
	}

	HTTPConfig struct {
		Port            string        `mapstructure:"port"`
		ReadTimeout     time.Duration `mapstructure:"read_timeout"`
		WriteTimeout    time.Duration `mapstructure:"write_timeout"`
		ShutdownTimeout time.Duration `mapstructure:"shutdown_timeout"`
	}
)

//func getPostgresURI(s *PostgresConfig) string {
//	return fmt.Sprintf("postgres://%s:%s@%s:%d/%s?sslmode=disable", s.Username, s.Password, s.Host, s.Port, s.Name)
//}

func LoadConfig(path string) (*Config, error) {
	_ = godotenv.Load()
	viper.SetConfigFile(path)

	viper.SetEnvPrefix("APP")
	viper.AutomaticEnv()
	viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

	if err := viper.ReadInConfig(); err != nil {
		return nil, err
	}

	var cfg Config
	if err := viper.Unmarshal(&cfg); err != nil {
		return nil, err
	}

	return &cfg, nil
}

const defaultConfigPath = "config/config.yaml"

func NewConfig() *Config {
	configPath := os.Getenv("CONFIG_PATH")
	if configPath == "" {
		configPath = defaultConfigPath
	}

	cfg, err := LoadConfig(configPath)
	if err != nil {
		panic(fmt.Sprintf("failed to load configuration: %v", err))
	}
	return cfg
}
