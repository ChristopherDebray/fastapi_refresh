from sqlalchemy.orm import Session
from sqlalchemy import select
from app.module.user.domain.ports.user_read_port import UserReadPort
from app.module.user.infrastructure.dtos.outputs import UserResponseDto
from app.module.user.infrastructure.persistence.user_model import UserModel

class UserReadSqlAlchemyRepository(UserReadPort):
    def __init__(self, db: Session) -> None:
        self.db = db

    def find_all(self) -> list[UserResponseDto]:
        return self.db.execute(select(UserModel)).scalars().all()

    def find_by_id(self, user_id: int) -> UserResponseDto | None:
        return self.db.get(UserModel, user_id)