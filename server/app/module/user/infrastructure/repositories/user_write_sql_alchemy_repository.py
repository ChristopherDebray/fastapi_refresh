from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions.unique_constraint_exceptions import UniqueConstraintException
from app.module.user.domain.ports.user_write_port import UserWritePort
from app.module.user.infrastructure.dtos.inputs import UserCreateDto, UserUpdateDto
from app.module.user.infrastructure.dtos.outputs import UserResponseDto
from app.module.user.infrastructure.persistence.user_model import UserModel

class UserWriteSqlAlchemyRepository(UserWritePort):
    def __init__(self, db: Session) -> None:
        self.db = db

    def save(self, dto: UserCreateDto) -> UserResponseDto:
        try:
            model = UserModel(email=dto.email, first_name=dto.first_name, last_name=dto.last_name)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return UserResponseDto(
                id=model.id,
                email=model.email,
                first_name=model.first_name,
                last_name=model.last_name,
            )
        except IntegrityError:
            self.db.rollback()
            raise UniqueConstraintException("email", dto.email)

    def update(self, dto: UserUpdateDto) -> UserResponseDto:
        model = self.db.get(UserModel, dto.id)
        for field, value in dto.model_dump(exclude_unset=True, exclude_none=True).items():
            if field != "id":
                setattr(model, field, value)
        self.db.commit()
        self.db.refresh(model)
        return UserResponseDto(
            id=model.id,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
        )
    
    def delete(self, user_id: int) -> None:
        model = self.db.get(UserModel, user_id)
        self.db.delete(model)
        self.db.commit()