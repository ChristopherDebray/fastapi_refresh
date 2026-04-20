from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.module.auth.application.use_cases.login_use_case import LoginUseCase
from app.module.auth.application.use_cases.logout_use_case import LogoutUseCase
from app.module.auth.application.use_cases.refresh_token_use_case import (
    RefreshTokenUseCase,
)
from app.module.auth.domain.ports.auth_read_port import AuthReadPort
from app.module.auth.domain.ports.auth_write_port import AuthWritePort
from app.module.auth.infrastructure.repositories.auth_read_sql_alchemy_repository import (
    AuthReadSqlAlchemyRepository,
)
from app.module.auth.infrastructure.repositories.auth_write_sql_alchemy_repository import (
    AuthWriteSqlAlchemyRepository,
)


def get_auth_read_repository(db: Session = Depends(get_db)) -> AuthReadPort:
    return AuthReadSqlAlchemyRepository(db)


def get_auth_write_repository(db: Session = Depends(get_db)) -> AuthWritePort:
    return AuthWriteSqlAlchemyRepository(db)


def get_login_use_case(
    read_repo: AuthReadPort = Depends(get_auth_read_repository),
    write_repo: AuthWritePort = Depends(get_auth_write_repository),
) -> LoginUseCase:
    return LoginUseCase(read_repo, write_repo)


def get_refresh_token_use_case(
    read_repo: AuthReadPort = Depends(get_auth_read_repository),
    write_repo: AuthWritePort = Depends(get_auth_write_repository),
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(read_repo, write_repo)


def get_logout_use_case(
    write_repo: AuthWritePort = Depends(get_auth_write_repository),
) -> LogoutUseCase:
    return LogoutUseCase(write_repo)
