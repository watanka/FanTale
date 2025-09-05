.PHONY: help install build-packages build-web build-all dev-web dev-web-prod lint-web

# FanTale Frontend Makefile (web app)
# Requires: pnpm (workspace root)

PORT ?= 3000

help:
	@echo "Targets:"
	@echo "  install          - Install workspace dependencies"
	@echo "  build-packages   - Build shared packages (@fantale/types, @fantale/api)"
	@echo "  build-web        - Build the Next.js web app (builds packages first)"
	@echo "  build-all        - Build packages and web app"
	@echo "  dev-web          - Run the Next.js dev server (override with PORT=$(PORT))"
	@echo "  dev-web-prod     - Start web app in production mode (build then start)"
	@echo "  lint-web         - Run Next.js lint for web app"

install:
	pnpm install

build-packages:
	pnpm -w -F @fantale/types build
	pnpm -w -F @fantale/api build

build-web: build-packages
	pnpm -C apps/web build

build-all: build-packages build-web

dev-web:
	exec pnpm -C apps/web exec next dev -p $(PORT)

dev-web-prod: build-web
	exec pnpm -C apps/web start

lint-web:
	pnpm -C apps/web lint
