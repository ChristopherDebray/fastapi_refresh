# Fastapi_refresh

For this project i will use the following in my docker compose

- postgis (postgres + extension)
- dpage/pgadmin4

I intend to inspire myself from another project to use part of it's domain rules to push myself on working on the architecture a bit, so i will use `postgis` for the geolocalisation tools

`dpage/pgadmin4` is for table db visualisation, i never tested it.

The project is mostly for start again working on fastapi, so i will not over compare / analyze each dependancy choices

- data validation : `pydantic` (it is the most commonly used)
- ORM : SQLAlchemy (with alembic for migrations)