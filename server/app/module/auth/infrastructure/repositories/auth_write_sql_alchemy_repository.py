from sqlalchemy import update
from sqlalchemy.orm import Session

from app.module.auth.domain.ports.auth_write_port import AuthWritePort
from app.module.user.infrastructure.persistence.user_model import UserModel


class AuthWriteSqlAlchemyRepository(AuthWritePort):
    def __init__(self, db: Session) -> None:
        self.db = db

    def save_refresh_token(self, user_id: int, refresh_token: str | None) -> None:
        self.db.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(refresh_token=refresh_token)
        )
        self.db.commit()
