.PHONY: help \
	install install-backend install-frontend \
	run-backend dev-backend fmt-backend lint-backend worker beat flower \
	build-packages build-frontend build-frontend-all dev-frontend dev-frontend-prod lint-frontend \
	dev

# Root Makefile that proxies to backend/ and frontend/ Makefiles
BACKEND_DIR ?= backend
FRONTEND_DIR ?= frontend

BACKEND_PORT ?= 8000
FRONTEND_PORT ?= 3000

help:
	@echo "FanTale root Makefile"
	@echo "\nBackend:"
	@echo "  make install-backend            # uv venv + sync"
	@echo "  make run-backend               # start API (PORT=$(BACKEND_PORT))"
	@echo "  make dev-backend               # auto-reload API (PORT=$(BACKEND_PORT))"
	@echo "  make fmt-backend               # ruff format"
	@echo "  make lint-backend              # ruff check"
	@echo "  make worker|beat|flower        # celery tools"
	@echo "\nFrontend:"
	@echo "  make install-frontend          # pnpm install"
	@echo "  make build-packages            # build shared packages"
	@echo "  make build-frontend            # build Next.js app"
	@echo "  make build-frontend-all        # build packages + app"
	@echo "  make dev-frontend              # dev server (PORT=$(FRONTEND_PORT))"
	@echo "  make dev-frontend-prod         # build then start"
	@echo "  make lint-frontend             # next lint"
	@echo "\nComposite:"
	@echo "  make install                   # install backend + frontend"
	@echo "  make dev                       # run backend+frontend concurrently"
	@echo "  make stop                      # stop backend+frontend dev servers"

# --- Composite ---
install: install-backend install-frontend

# Run both dev servers concurrently (press Ctrl+C to stop all)
# Use BACKEND_PORT and FRONTEND_PORT to override.
dev:
	$(MAKE) dev-backend & \
	$(MAKE) dev-frontend & \
	wait

# --- Backend proxies ---
install-backend:
	$(MAKE) -C $(BACKEND_DIR) install

run-backend:
	$(MAKE) -C $(BACKEND_DIR) run PORT=$(BACKEND_PORT)

dev-backend:
	$(MAKE) -C $(BACKEND_DIR) dev PORT=$(BACKEND_PORT)

fmt-backend:
	$(MAKE) -C $(BACKEND_DIR) fmt

lint-backend:
	$(MAKE) -C $(BACKEND_DIR) lint

worker:
	$(MAKE) -C $(BACKEND_DIR) worker

beat:
	$(MAKE) -C $(BACKEND_DIR) beat

flower:
	$(MAKE) -C $(BACKEND_DIR) flower

# --- Frontend proxies ---
install-frontend:
	$(MAKE) -C $(FRONTEND_DIR) install

build-packages:
	$(MAKE) -C $(FRONTEND_DIR) build-packages

build-frontend:
	$(MAKE) -C $(FRONTEND_DIR) build-web

build-frontend-all:
	$(MAKE) -C $(FRONTEND_DIR) build-all

dev-frontend:
	$(MAKE) -C $(FRONTEND_DIR) dev-web PORT=$(FRONTEND_PORT)

dev-frontend-prod:
	$(MAKE) -C $(FRONTEND_DIR) dev-web-prod

lint-frontend:
	$(MAKE) -C $(FRONTEND_DIR) lint-web

# Stop both backend and frontend dev servers bound to BACKEND_PORT and FRONTEND_PORT
stop:
	-@echo "Stopping servers on BACKEND_PORT=$(BACKEND_PORT), FRONTEND_PORT=$(FRONTEND_PORT)"
	-@fuser -k $(BACKEND_PORT)/tcp 2>/dev/null || true
	-@fuser -k $(FRONTEND_PORT)/tcp 2>/dev/null || true
