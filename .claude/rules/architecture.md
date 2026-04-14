# Règles d'architecture — à respecter strictement

`entity` sera remplacé par le nom de l'entité cible

## Imports interdits
- Ne jamais importer EntityModel dans presentation/
- Ne jamais importer EntityModel dans application/use_cases/
- Ne jamais utiliser db: Session directement dans les routes

## Ce que chaque couche retourne
- Repository (adapter) → toujours EntityResponseDto ou autre dto de réponse, jamais EntityModel
- Use case → toujours EntityResponseDto ou autre dto de réponse, jamais EntityModel
- Route → toujours EntityResponseDto avec response_model=EntityResponseDto

## Ports
- Les ports (Protocol) sont dans domain/ports/
- Les adapters (implémentations) sont dans infrastructure/repositories/
- Le type de retour dans dependencies.py est toujours le Port, pas l'adapter :
  def get_Entity_read_repository(...) -> EntityReadPort  ✓
  def get_Entity_read_repository(...) -> EntityReadSqlAlchemyRepository  ✗

## DTOs
- inputs.py : EntityCreateDto, EntityUpdateDto (Pydantic BaseModel avec validation)
- outputs.py : EntityResponseDto (jamais de champ password dedans)
- EntityResponseDto a model_config = {"from_attributes": True}

## Injection de dépendances
- Chaque use case a sa factory dans presentation/dependencies.py
- Format : def get_<action>_use_case(repo = Depends(...)) -> UseCaseClass
- Dans les routes : use_case: UseCaseClass = Depends(get_<action>_use_case)

Par exemple :

```python
def get_user_write_repository(db: Session = Depends(get_db)) -> UserWritePort:
    return UserWriteSqlAlchemyRepository(db)
```

## Validation
- Toujours utiliser EmailStr pour les emails
- Toujours utiliser Field(min_length=..., max_length=...) pour les strings

## Exceptions
- Erreurs métier → lever une classe héritant de Exception dans app/core/exceptions/
- Violation unique constraint → UniqueConstraintException via integrity_error_helper.py
- Toujours db.rollback() avant raise sur IntegrityError
- HTTPException uniquement dans les use cases pour 404, jamais dans les repositories

## Sécurité
- Hash des passwords via app/core/security/encrypt_service.py (bcrypt)
- Jamais stocker ou retourner le password en clair
- EntityResponseDto ne contient jamais de champ privé (password par exemple) sauf exception (repository d'auth pour check le mot de passe avec le hash par exemple)

## Exemple de structure d'un module

```
server/app/module/Entity/
├── application
│   └── use_cases
│       ├── create_Entity_use_case.py
│       ├── delete_Entity_use_case.py
│       ├── get_Entitys_use_case.py
│       ├── get_Entity_use_case.py
│       └── update_Entity_use_case.py
├── domain
│   ├── enums.py
│   ├── __init__.py
│   ├── ports
│   │   ├── __init__.py
│   │   ├── Entity_read_port.py
│   │   └── Entity_write_port.py
│   └── Entity.py
├── infrastructure
│   ├── dtos
│   │   ├── __init__.py
│   │   ├── inputs.py
│   │   ├── outputs.py
│   ├── __init__.py
│   ├── persistence
│   │   ├── __init__.py
│   │   └── Entity_model.py
│   └── repositories
│       ├── __init__.py
│       ├── Entity_read_sql_alchemy_repository.py
│       └── Entity_write_sql_alchemy_repository.py
└── presentation
    ├── dependancies.py
    ├── __init__.py
    └── routes.py
```