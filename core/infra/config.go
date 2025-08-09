package infra

import (
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/joho/godotenv"
	"github.com/spf13/viper"
)

type (
	Config struct {
		App      AppConfig      `mapstructure:"app"`
		HTTP     HTTPConfig     `mapstructure:"http"`
		Database DatabaseConfig `mapstructure:"database"`
		Web      WebConfig      `mapstructure:"web"`
	}

	DatabaseConfig struct {
		Name     string `mapstructure:"name"`
		Username string `mapstructure:"username"`
		Port     int32  `mapstructure:"port"`
		Password string `mapstructure:"password"`
		Host     string `mapstructure:"host"`
	}

	WebConfig struct {
		Host     string `mapstructure:"host"`
		Password string `mapstructure:"password"`
		Port     int32  `mapstructure:"port"`
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

func DBURL(s *DatabaseConfig) string {
	return "postgres://" + s.Username + ":" + s.Password + "@" + s.Host + ":" + string(s.Port) + "/" + s.Name
}

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

const defaultConfigPath = "configs/config.yaml"

func GetConfig() *Config {
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
