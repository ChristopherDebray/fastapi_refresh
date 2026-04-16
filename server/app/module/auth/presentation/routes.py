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

COOKIE_NAME = "access_token"
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
        key=COOKIE_NAME,
        value=result.access_token,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="strict" if IS_PRODUCTION else "lax",
        max_age=settings.JWT_EXPIRE_MINUTES * 60,
    )
    return result.user


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    use_case: LogoutUseCase = Depends(get_logout_use_case),
) -> None:
    use_case.execute()
    response.delete_cookie(key=COOKIE_NAME)
