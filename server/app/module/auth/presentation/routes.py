from fastapi import APIRouter, Depends, Response, status

from app.core.config import settings
from app.core.routing import PublicAPIRoute
from app.module.auth.application.use_cases.login_use_case import LoginUseCase
from app.module.auth.application.use_cases.logout_use_case import LogoutUseCase
from app.module.auth.infrastructure.dtos.inputs import LoginDto
from app.module.auth.presentation.dependancies import (
    get_login_use_case,
    get_logout_use_case,
)
from app.module.user.infrastructure.dtos.outputs import UserResponseDto
from server.app.core.security.auth_dependencies import get_current_user
from server.app.core.security.token_payload import TokenPayloadDto

ACCESS_TOKEN_COOKIE = "access_token"
REFRESH_TOKEN_COOKIE = "refresh_token"
IS_PRODUCTION = settings.ENVIRONMENT == "production"

router = APIRouter(prefix="/api/auth", tags=["auth"], route_class=PublicAPIRoute)


@router.post("/login", response_model=UserResponseDto, status_code=status.HTTP_200_OK)
def login(
    payload: LoginDto,
    response: Response,
    use_case: LoginUseCase = Depends(get_login_use_case),
) -> UserResponseDto:
    result = use_case.execute(payload)
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE,
        value=result.access_token,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="strict" if IS_PRODUCTION else "lax",
        max_age=settings.JWT_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE,
        value=result.refresh_token,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="strict" if IS_PRODUCTION else "lax",
        # Ici mettre 1 semaine
        max_age=settings.JWT_EXPIRE_MINUTES * 60,
    )

    return result.user


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    use_case: LogoutUseCase = Depends(get_logout_use_case),
) -> None:
    use_case.execute()
    response.delete_cookie(key=ACCESS_TOKEN_COOKIE)
    response.delete_cookie(key=REFRESH_TOKEN_COOKIE)

@router.get(
    "/me",
    response_model=UserResponseDto,
    status_code=status.HTTP_200_OK,
)
def me(
    current_user: TokenPayloadDto = Depends(get_current_user),
) -> UserResponseDto:
    """Retourne les infos de l'utilisateur connecté depuis le token"""
    return UserResponseDto(
        id=current_user.id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        role=current_user.role
    )
