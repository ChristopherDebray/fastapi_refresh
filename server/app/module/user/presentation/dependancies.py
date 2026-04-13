from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.module.user.application.use_cases.create_user_use_case import CreateUserUseCase
from app.module.user.application.use_cases.delete_user_use_case import DeleteUserUseCase
from app.module.user.application.use_cases.get_user_use_case import GetUserUseCase
from app.module.user.application.use_cases.get_users_use_case import GetUsersUseCase
from app.module.user.application.use_cases.update_user_use_case import UpdateUserUseCase
from app.module.user.domain.ports.user_read_port import UserReadPort
from app.module.user.domain.ports.user_write_port import UserWritePort
from app.module.user.infrastructure.dtos.outputs import UserResponseDto
from app.module.user.infrastructure.repositories.user_read_sql_alchemy_repository import UserReadSqlAlchemyRepository
from app.module.user.infrastructure.repositories.user_write_sql_alchemy_repository import UserWriteSqlAlchemyRepository

def get_user_read_repository(db: Session = Depends(get_db)) -> UserReadPort:
    return UserReadSqlAlchemyRepository(db)

def get_user_write_repository(db: Session = Depends(get_db)) -> UserWritePort:
    return UserWriteSqlAlchemyRepository(db)

def get_create_user_use_case(
    write_repo: UserWritePort = Depends(get_user_write_repository)
) -> CreateUserUseCase:
    return CreateUserUseCase(write_repo)

def get_update_user_use_case(
    read_repo: UserReadPort = Depends(get_user_read_repository),
    write_repo: UserWritePort = Depends(get_user_write_repository)
) -> UpdateUserUseCase:
    return UpdateUserUseCase(write_repo, read_repo)

def get_delete_user_use_case(
    read_repo: UserReadPort = Depends(get_user_read_repository),
    write_repo: UserWritePort = Depends(get_user_write_repository)
) -> DeleteUserUseCase:
    return DeleteUserUseCase(write_repo, read_repo)

def get_get_user_use_case(
    read_repo: UserReadPort = Depends(get_user_read_repository),       
) -> UserResponseDto:
    return GetUserUseCase(read_repo)

def get_get_users_use_case(
    read_repo: UserReadPort = Depends(get_user_read_repository),       
) -> UserResponseDto:
    return GetUsersUseCase(read_repo)