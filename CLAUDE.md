# Fastapi Refresh — Contexte projet

## Stack
Python 3.14 · FastAPI · SQLAlchemy 2.0 · PostgreSQL (PostGIS) · Alembic · Docker Compose · Pydantic v2

## Lancer le projet
docker compose up --build

## Commandes utiles
make run-migration-generate NAME="description"
make run-migration-upgrade
make run-db-refresh         # drop schema + migrations + seeds
make run-seeds

## Architecture
Hexagonale par module. Chaque module dans app/module/<nom>/ contient :
- domain/         → entités pures, ports (interfaces), enums
- application/    → use cases uniquement, pas d'ORM ici
- infrastructure/ → persistence (SQLAlchemy models), repositories (adapters), DTOs
- presentation/   → routes FastAPI, dependencies.py

## Réponse API
Toutes les réponses sont wrappées par ResponseWrapperMiddleware :
{ "isSuccess": bool, "path": str, "data": ... }
Les erreurs sont gérées par exception_handler.py — même format avec "error" au lieu de "data".

## Tests
docker compose exec server pytest tests/ -v