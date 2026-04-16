from sqlalchemy import select
from sqlalchemy.orm import Session

from app.module.user.domain.ports.user_read_port import UserReadPort
from app.module.user.infrastructure.dtos.outputs import UserResponseDto
from app.module.user.infrastructure.persistence.user_model import UserModel


class UserReadSqlAlchemyRepository(UserReadPort):
    def __init__(self, db: Session) -> None:
        self.db = db

    def find_all(self) -> list[UserResponseDto]:
        models = self.db.execute(select(UserModel)).scalars().all()
        return [UserResponseDto.model_validate(m) for m in models]

    def find_by_id(self, user_id: int) -> UserResponseDto | None:
        model = self.db.get(UserModel, user_id)
        return UserResponseDto.model_validate(model) if model else None
