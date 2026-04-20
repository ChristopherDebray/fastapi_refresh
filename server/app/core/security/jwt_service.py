from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.config import settings
from app.core.security.token_payload import CreateAccessTokenDto, CreateRefreshTokenDto, RefreshTokenPayloadDto, TokenPayloadDto


class JwtService:
    @staticmethod
    def create_access_token(dto: CreateAccessTokenDto) -> str:
        expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        payload = {
            "id": str(dto.user_id),
            "sub": str(dto.user_id),
            "email": dto.email,
            "first_name": dto.first_name,
            "last_name": dto.last_name,
            "role": dto.role,
            "exp": expire,
        }
        return jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def create_refresh_token(dto: CreateRefreshTokenDto) -> str:
        expire = datetime.now(UTC) + timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS)
        payload = {"user_id": str(dto.user_id), "email": dto.email, "exp": expire}
        return jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def decode_access_token(token: str) -> TokenPayloadDto:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return TokenPayloadDto(
            id=int(payload["sub"]),
            sub=int(payload["sub"]),
            email=payload["email"],
            first_name=payload["first_name"],
            last_name=payload["last_name"],
            role=payload["role"],
        )

    @staticmethod
    def decode_refresh_token(token: str) -> RefreshTokenPayloadDto:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return RefreshTokenPayloadDto(
            user_id=int(payload["user_id"]),
            email=payload["email"],
        )
