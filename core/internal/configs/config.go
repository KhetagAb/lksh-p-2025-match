package configs

import (
	"github.com/joho/godotenv"
	"strings"
	"time"

	"github.com/spf13/viper"
)

type (
	Config struct {
		App      AppConfig      `mapstructure:"app"`
		HTTP     HTTPConfig     `mapstructure:"http"`
		Database DatabaseConfig `mapstructure:"database"`
		Web      WebConfig      `mapstructure:"web"`
		TgBot    TgBotConfig    `mapstructure:"tg"`
	}

	DatabaseConfig struct {
		Name     string `mapstructure:"name"`
		Username string `mapstructure:"username"`
		Port     int64  `mapstructure:"port"`
		Password string `mapstructure:"password"`
		Host     string `mapstructure:"host"`
	}

	WebConfig struct {
		Host     string `mapstructure:"host"`
		Password string `mapstructure:"password"`
		Port     int64  `mapstructure:"port"`
	}
	TgBotConfig struct {
		Token string `mapstructure:"token"`
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

	Users struct {
		Users []string `mapstructure:"users"`
	}
)

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

func LoadUsers(path string) (*Users, error) {
	v := viper.New()
	v.SetDefault("users", []string{"English"})
	v.SetConfigFile(path)

	if err := v.ReadInConfig(); err != nil {
		return nil, err
	}

	var cfg Users
	if err := v.Unmarshal(&cfg); err != nil {
		return nil, err
	}

	return &cfg, nil
}
