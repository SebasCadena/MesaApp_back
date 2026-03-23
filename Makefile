.PHONY: help up down logs migrate migration seed dev

help:
	@echo "Comandos disponibles:"
	@echo "  make up                -> Levanta Postgres + Adminer en segundo plano"
	@echo "  make down              -> Baja contenedores"
	@echo "  make logs              -> Sigue logs del servicio db"
	@echo "  make migrate           -> Aplica migraciones (alembic upgrade head)"
	@echo "  make migration msg=\"descripcion\" -> Crea migracion autogenerada"
	@echo "  make seed              -> Ejecuta semillas"
	@echo "  make dev               -> Inicia FastAPI en modo reload"

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f db

migrate:
	alembic upgrade head

migration:
	$(if $(strip $(msg)),,$(error Uso: make migration msg="descripcion"))
	alembic revision --autogenerate -m "$(msg)"

seed:
	python -m app.seeds

dev:
	uvicorn app.main:app --reload --port 8000