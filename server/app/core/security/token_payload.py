from pydantic import BaseModel

from app.module.user.domain.enums import UserRole


class CreateAccessTokenDto(BaseModel):
    user_id: int
    email: str
    first_name: str
    last_name: str
    role: UserRole


class CreateRefreshTokenDto(BaseModel):
    user_id: int
    email: str


class TokenPayloadDto(BaseModel):
    id: int
    sub: int
    email: str
    first_name: str
    last_name: str
    role: UserRole


class RefreshTokenPayloadDto(BaseModel):
    user_id: int
    email: str
