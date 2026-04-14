### Colors
NOCOLOR=\033[0m
RED=\033[0;31m
GREEN=\033[0;32m
ORANGE=\033[0;33m
BLUE=\033[0;34m
CYAN=\033[0;36m

### Executables
DOCKER_SERVER_CLI=docker compose exec -it server bash

## CONFIG
run-pip-install:
	@printf "🔍 $(CYAN)Install project requirements : ${NAME} ${NOCOLOR} \n"
	${DOCKER_SERVER_CLI} -c "pip install -r requirements.txt"

## MIGRATION
run-migration-generate:
ifdef NAME
	@printf "🔍 $(CYAN)Generating migration : ${NAME} ${NOCOLOR} \n"
	${DOCKER_SERVER_CLI} -c "alembic revision --autogenerate -m '${NAME}'"
else
	@printf "❌ ${RED}You must have a NAME for your migration${NOCOLOR} \n"
endif

run-migration-upgrade:
	@printf "🚀 $(GREEN)Applying all pending migrations${NOCOLOR} \n"
	${DOCKER_SERVER_CLI} -c "alembic upgrade head"

run-migration-upgrade-one:
	@printf "🚀 $(GREEN)Applying next migration${NOCOLOR} \n"
	${DOCKER_SERVER_CLI} -c "alembic upgrade +1"

run-migration-downgrade:
	@printf "⬇️  $(ORANGE)Rolling back one migration${NOCOLOR} \n"
	${DOCKER_SERVER_CLI} -c "alembic downgrade -1"

run-migration-history:
	@printf "📜 $(CYAN)Migration history${NOCOLOR} \n"
	${DOCKER_SERVER_CLI} -c "alembic history"

run-migration-current:
	@printf "📍 $(CYAN)Current migration${NOCOLOR} \n"
	${DOCKER_SERVER_CLI} -c "alembic current"

## DATABASE
run-seeds:
	@printf "🌱 $(GREEN)Running seeds${NOCOLOR} \n"
	${DOCKER_SERVER_CLI} -c "python seeds/run_seeds.py"

run-db-refresh:
	@printf "🔄 $(RED)Full refresh : migrations + seeds${NOCOLOR} \n"
	${DOCKER_SERVER_CLI} -c "alembic downgrade base && alembic upgrade head && python seeds/run_seeds.py"