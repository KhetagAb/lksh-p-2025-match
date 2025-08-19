//go:build tools
// +build tools

package main

import (
	_ "github.com/google/wire/cmd/wire"
	_ "github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen"
	_ "github.com/pressly/goose/v3/cmd/goose"
)
