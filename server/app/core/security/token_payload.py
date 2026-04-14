from pydantic import BaseModel

from app.module.user.domain.enums import UserRole


class TokenPayloadDto(BaseModel):
    sub: int
    email: str
    role: UserRole
