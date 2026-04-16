from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.config import settings
from app.core.security.token_payload import TokenPayloadDto


class JwtService:
    @staticmethod
    def create_access_token(user_id: int, email: str, role: str) -> str:
        expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
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
            sub=int(payload["sub"]),
            email=payload["email"],
            role=payload["role"],
        )
