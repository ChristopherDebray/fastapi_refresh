from pydantic import BaseModel

from app.module.user.domain.enums import UserRole


class TokenPayloadDto(BaseModel):
    id: int
    sub: int
    email: str
    first_name: UserRole
    last_name: UserRole
    role: UserRole
