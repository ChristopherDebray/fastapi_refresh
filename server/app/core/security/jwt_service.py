from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.config import settings
from app.core.security.token_payload import TokenPayloadDto


class JwtService:
    @staticmethod
    def create_access_token(user_id: int, email: str, role: str) -> str:
        """
        @static
        """
        expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        payload = {"sub": str(user_id), "email": email, "role": role, "exp": expire}
        return jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def create_refresh_token(user_id: int, email: str, role: str) -> str:
        expire = datetime.now(UTC) + timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS)
        payload = {"sub": str(user_id), "email": email, "role": role, "exp": expire}
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
