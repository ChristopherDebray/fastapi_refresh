# Conventions de nommage et style

`entity` sera remplacé par le nom de l'entité cible

## Fichiers
- entity_read_port.py, entity_write_port.py (domain/ports/)
- entity_read_sql_alchemy_repository.py (infrastructure/repositories/)
- entity_model.py (infrastructure/persistence/)
- inputs.py, outputs.py (infrastructure/dtos/)
- create_entity_use_case.py (application/use_cases/)

## Classes
- Ports : EntityReadPort, EntityWritePort (Protocol)
- Adapters : EntityReadSqlAlchemyRepository, EntityWriteSqlAlchemyRepository
- Use cases : CreateEntityUseCase, UpdateEntityUseCase, DeleteEntityUseCase
- DTOs : EntityCreateDto, EntityUpdateDto, EntityResponseDto
- Model SQLAlchemy : EntityModel

## Enums
- Définis dans domain/enums.py
- Toujours str + enum.Enum pour compatibilité Pydantic/SQLAlchemy
- server_default ET default sur les colonnes enum dans EntityModel

## Migrations Alembic
- Toujours checkfirst=True sur create/drop des types enum PostgreSQL
- Toujours ajouter server_default pour les colonnes NOT NULL ajoutées sur table existante
- Toujours ajouter les enums requis en bdd si ils ne sont pas auto généré dans la migration
- Vérifier le fichier généré avant upgrade

## Middleware (ordre dans main.py)
1. CORSMiddleware
2. LoggingMiddleware  
3. ResponseWrapperMiddleware
4. exception_handler (UniqueConstraintException)
5. exception_handler (RequestValidationError)
6. exception_handler (HTTPException)
7. exception_handler (Exception) — toujours en dernier