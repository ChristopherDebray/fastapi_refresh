from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.module.auth.application.use_cases.login_use_case import LoginUseCase
from app.module.auth.application.use_cases.logout_use_case import LogoutUseCase
from app.module.auth.domain.ports.auth_read_port import AuthReadPort
from app.module.auth.infrastructure.repositories.auth_sql_alchemy_repository import AuthSqlAlchemyRepository


def get_auth_read_repository(db: Session = Depends(get_db)) -> AuthReadPort:
    return AuthSqlAlchemyRepository(db)


def get_login_use_case(
    repo: AuthReadPort = Depends(get_auth_read_repository),
) -> LoginUseCase:
    return LoginUseCase(repo)


def get_logout_use_case() -> LogoutUseCase:
    return LogoutUseCase()
