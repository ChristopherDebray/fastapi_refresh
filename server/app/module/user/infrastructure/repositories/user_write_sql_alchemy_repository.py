from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions.integrity_error_helper import (
    extract_field_from_integrity_error,
)
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
            model = UserModel(
                email=dto.email, first_name=dto.first_name, last_name=dto.last_name
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return UserResponseDto.model_validate(model)
        except IntegrityError as e:
            self.db.rollback()
            field = extract_field_from_integrity_error(e)
            raise UniqueConstraintException(
                field, getattr(dto, field, "unknown")
            ) from e

    def update(self, dto: UserUpdateDto) -> UserResponseDto:
        try:
            model = self.db.get(UserModel, dto.id)
            assert model is not None
            for field, value in dto.model_dump(
                exclude_unset=True, exclude_none=True
            ).items():
                if field != "id":
                    setattr(model, field, value)
            self.db.commit()
            self.db.refresh(model)
            return UserResponseDto.model_validate(model)
        except IntegrityError as e:
            self.db.rollback()
            field = extract_field_from_integrity_error(e)
            raise UniqueConstraintException(
                field, getattr(dto, field, "unknown")
            ) from e

    def delete(self, user_id: int) -> None:
        model = self.db.get(UserModel, user_id)
        self.db.delete(model)
        self.db.commit()
