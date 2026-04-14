from sqlalchemy import select
from sqlalchemy.orm import Session

from app.module.auth.domain.ports.auth_read_port import AuthReadPort
from app.module.auth.infrastructure.dtos.outputs import AuthUserWithPasswordDto
from app.module.user.infrastructure.persistence.user_model import UserModel


class AuthSqlAlchemyRepository(AuthReadPort):
    def __init__(self, db: Session) -> None:
        self.db = db

    def find_by_email(self, email: str) -> AuthUserWithPasswordDto | None:
        model = self.db.execute(
            select(UserModel).where(UserModel.email == email)
        ).scalar_one_or_none()
        if model is None:
            return None
        return AuthUserWithPasswordDto(
            id=model.id,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            password=model.password,
        )
