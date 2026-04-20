from pydantic import BaseModel, ConfigDict

from app.module.user.domain.enums import UserRole
from app.module.user.infrastructure.dtos.outputs import UserResponseDto


class AuthUserWithPasswordDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    first_name: str
    last_name: str
    password: str
    refresh_token: str | None
    role: UserRole


class AuthResponseDto(BaseModel):
    user: UserResponseDto
    access_token: str
    refresh_token: str
