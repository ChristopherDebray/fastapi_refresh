from fastapi import HTTPException, status

from app.core.security.jwt_service import JwtService
from app.core.security.token_payload import CreateAccessTokenDto, CreateRefreshTokenDto
from app.module.auth.domain.ports.auth_read_port import AuthReadPort
from app.module.auth.domain.ports.auth_write_port import AuthWritePort
from app.module.auth.infrastructure.dtos.outputs import AuthResponseDto
from app.module.user.infrastructure.dtos.outputs import UserResponseDto


class RefreshTokenUseCase:
    def __init__(
        self, auth_read_repo: AuthReadPort, auth_write_repo: AuthWritePort
    ) -> None:
        self.auth_read_repo = auth_read_repo
        self.auth_write_repo = auth_write_repo

    def execute(self, refresh_token: str) -> AuthResponseDto:
        """
        Validate the refresh token and generate a new access + refresh token

        Args:
            refresh_token: The JWT refresh token from the cookie

        Returns:
            AuthResponseDto with user, access_token, and new refresh_token
        """

        print(f"${refresh_token}")
        try:
            payload = JwtService.decode_refresh_token(refresh_token)
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            ) from err

        user = self.auth_read_repo.find_by_id(payload.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        if user.refresh_token != refresh_token:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        access_token_dto = CreateAccessTokenDto(
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
        )
        new_access_token = JwtService.create_access_token(access_token_dto)

        refresh_token_dto = CreateRefreshTokenDto(
            user_id=user.id,
            email=user.email,
        )
        new_refresh_token = JwtService.create_refresh_token(refresh_token_dto)
        self.auth_write_repo.save_refresh_token(user.id, new_refresh_token)

        return AuthResponseDto(
            user=UserResponseDto(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                role=user.role,
            ),
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )
