from pydantic import BaseModel, ConfigDict
from app.module.user.domain.enums import UserRole


class UserResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    first_name: str
    last_name: str
    role: UserRole
