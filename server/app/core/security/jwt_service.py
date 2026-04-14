from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings


class JwtService:
    @staticmethod
    def create_access_token(subject: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        payload = {"sub": str(subject), "exp": expire}
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
