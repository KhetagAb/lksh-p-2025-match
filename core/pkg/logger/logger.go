package logger

import (
	"context"
	"os"
	"sync"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

const (
	DebugLevel = "debug"
	InfoLevel  = "info"
	WarnLevel  = "warn"
	ErrorLevel = "error"
	FatalLevel = "fatal"
)

var (
	defaultLogger *zap.Logger
	sugar         *zap.SugaredLogger
	once          sync.Once
)

func Init(serviceName, level string) {
	once.Do(func() {
		var zapLevel zapcore.Level
		switch level {
		case DebugLevel:
			zapLevel = zapcore.DebugLevel
		case InfoLevel:
			zapLevel = zapcore.InfoLevel
		case WarnLevel:
			zapLevel = zapcore.WarnLevel
		case ErrorLevel:
			zapLevel = zapcore.ErrorLevel
		case FatalLevel:
			zapLevel = zapcore.FatalLevel
		default:
			zapLevel = zapcore.InfoLevel
		}

		encoderConfig := zapcore.EncoderConfig{
			TimeKey:        "time",
			LevelKey:       "level",
			NameKey:        "logger",
			CallerKey:      "caller",
			FunctionKey:    zapcore.OmitKey,
			MessageKey:     "msg",
			StacktraceKey:  "stacktrace",
			LineEnding:     zapcore.DefaultLineEnding,
			EncodeLevel:    zapcore.LowercaseLevelEncoder,
			EncodeTime:     zapcore.ISO8601TimeEncoder,
			EncodeDuration: zapcore.StringDurationEncoder,
			EncodeCaller:   zapcore.ShortCallerEncoder,
		}

		core := zapcore.NewCore(
			zapcore.NewJSONEncoder(encoderConfig),
			zapcore.AddSync(os.Stdout),
			zapLevel,
		)

		defaultLogger = zap.New(core,
			zap.AddCaller(),
			zap.AddCallerSkip(1),
			zap.Fields(zapcore.Field{
				Key:    "service",
				Type:   zapcore.StringType,
				String: serviceName,
			}),
		)

		sugar = defaultLogger.Sugar()
	})
}

func Info(_ context.Context, msg string) {
	defaultLogger.Info(msg)
}

func Infof(_ context.Context, format string, args ...interface{}) {
	sugar.Infof(format, args...)
}

func Warn(_ context.Context, msg string) {
	defaultLogger.Warn(msg)
}

func Warnf(_ context.Context, format string, args ...interface{}) {
	sugar.Warnf(format, args...)
}

func Error(_ context.Context, msg string) {
	defaultLogger.Error(msg)
}

func Errorf(_ context.Context, format string, args ...interface{}) {
	sugar.Errorf(format, args...)
}

func Fatal(_ context.Context, msg string) {
	defaultLogger.Fatal(msg)
}

func Fatalf(_ context.Context, format string, args ...interface{}) {
	sugar.Fatalf(format, args...)
}

// Sync сбрасывает буферизованные логи
func Sync() error {
	return defaultLogger.Sync()
}
