#!/bin/bash
set -e

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # нет цвета

print_status() {
  local msg=$1
  local status=$2
  local color=$3
  printf "%-30s: %b%s%b\n" "$msg" "$color" "$status" "$NC"
}

version=$(oapi-codegen --version 2>/dev/null | tail -n1 || echo "unknown")
print_status "Oapi-codegen version" "$version" "$BLUE"

if oapi-codegen -config api/config.yaml api/openapi.yaml; then
  print_status "Generating OpenAPI code" "OK" "$GREEN"
else
  print_status "Generating OpenAPI code" "FAILED" "$RED"
  exit 1
fi

if (cd internal/generated/app && wire 2> /dev/null); then
  print_status "Generating Wire code" "OK" "$GREEN"
else
  print_status "Generating Wire code" "FAILED" "$RED"
  exit 1
fi

print_status "Code generation completed" "OK" "$GREEN"
