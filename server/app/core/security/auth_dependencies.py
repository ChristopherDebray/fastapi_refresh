from collections.abc import Callable

from fastapi import Depends, HTTPException, Request, status

from app.core.security.token_payload import TokenPayloadDto
from app.module.user.domain.enums import UserRole


def get_current_user(request: Request) -> TokenPayloadDto:
    user: TokenPayloadDto | None = getattr(request.state, "user", None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    return user


def require_roles(*roles: UserRole) -> Callable[..., TokenPayloadDto]:
    def dependency(
        user: TokenPayloadDto = Depends(get_current_user),
    ) -> TokenPayloadDto:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )
        return user

    return dependency
