---
name: generate-module
description: Génère le scaffold complet d'un module hexagonal FastAPI
disable-model-invocation: true
---
<!--
USAGE:
  /generate-module Product
  /generate-module Order
  /generate-module BlogPost    → snake: blog_post, plural: blog_posts
-->
Phrases courtes. Pas de politesses. Termes techniques intacts.

## Argument requis

`$ARGUMENTS` = nom de l'entité en PascalCase (ex: `Product`, `Order`)
Si absent → demander avant de continuer.

Dériver automatiquement :
- snake_case : `product`, `order`
- plural snake_case : `products`, `orders` (ajouter `s` sauf irréguliers évidents)

## Fichiers à générer

Tous sous `server/app/module/<snake>/` :

### domain/
- `<snake>.py` — dataclass pure (pas d'ORM), champs sans id si entité nouvelle
- `enums.py` — vide ou avec enums si mentionnés dans $ARGUMENTS, format `class XEnum(str, enum.Enum)`
- `ports/<snake>_read_port.py` — Protocol avec `find_all`, `find_by_id`
- `ports/<snake>_write_port.py` — Protocol avec `save`, `update`, `delete`
- `ports/__init__.py`, `__init__.py`

### infrastructure/dtos/
- `inputs.py` — `<Entity>CreateDto`, `<Entity>UpdateDto` (Pydantic, Field avec validations)
- `outputs.py` — `<Entity>ResponseDto` (model_config from_attributes, jamais de password)
- `__init__.py`

### infrastructure/persistence/
- `<snake>_model.py` — SQLAlchemy 2.0 (mapped_column, Mapped), hérite de Base

### infrastructure/repositories/
- `<snake>_read_sql_alchemy_repository.py` — implémente le ReadPort
- `<snake>_write_sql_alchemy_repository.py` — implémente le WritePort
- `__init__.py`

### infrastructure/`__init__.py`

### application/use_cases/
- `create_<snake>_use_case.py`
- `get_<plural>_use_case.py`
- `get_<snake>_use_case.py`
- `update_<snake>_use_case.py`
- `delete_<snake>_use_case.py`
- `__init__.py`

### application/`__init__.py`

### presentation/
- `routes.py` — APIRouter, 5 routes CRUD, response_model=<Entity>ResponseDto
- `dependancies.py` — factories pour chaque use case, retour typé avec le Port (jamais l'adapter)
- `__init__.py`

## Règles à respecter

- Repositories retournent toujours des DTOs, jamais des EntityModel
- Use cases lèvent HTTPException(404) si entité non trouvée, jamais les repositories
- `UniqueConstraintException` + `db.rollback()` avant raise sur IntegrityError dans les write repos
- Injection via `Depends` dans routes, type hint = Port
- EmailStr si champ email, Field(min_length=, max_length=) sur tous les strings
- Enums : `str + enum.Enum`, `server_default` ET `default` dans EntityModel

## Après génération

Afficher :
1. Liste des fichiers créés
2. Rappel d'enregistrer le router dans `main.py` : `app.include_router(<snake>_router, prefix="/api/<plural>", tags=["<Entity>"])`
3. Rappel de générer la migration : `make run-migration-generate NAME="add_<snake>_table"`

$ARGUMENTS
