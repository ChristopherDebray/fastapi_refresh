from fastapi import HTTPException, status

from app.core.security.encrypt_service import EncryptService
from app.core.security.jwt_service import JwtService
from app.core.security.token_payload import CreateAccessTokenDto, CreateRefreshTokenDto
from app.module.auth.domain.ports.auth_read_port import AuthReadPort
from app.module.auth.domain.ports.auth_write_port import AuthWritePort
from app.module.auth.infrastructure.dtos.inputs import LoginDto
from app.module.auth.infrastructure.dtos.outputs import AuthResponseDto
from app.module.user.infrastructure.dtos.outputs import UserResponseDto


class LoginUseCase:
    def __init__(
        self, auth_read_repo: AuthReadPort, auth_write_repo: AuthWritePort
    ) -> None:
        self.auth_read_repo = auth_read_repo
        self.auth_write_repo = auth_write_repo

    def execute(self, dto: LoginDto) -> AuthResponseDto:
        user = self.auth_read_repo.find_by_email(dto.email)
        if user is None or not EncryptService.verify(dto.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        token_dto = CreateAccessTokenDto(
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
        )
        access_token = JwtService.create_access_token(token_dto)

        refresh_token_dto = CreateRefreshTokenDto(
            user_id=user.id,
            email=user.email,
        )
        refresh_token = JwtService.create_refresh_token(refresh_token_dto)
        self.auth_write_repo.save_refresh_token(user.id, refresh_token)

        return AuthResponseDto(
            user=UserResponseDto(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                role=user.role,
            ),
            access_token=access_token,
            refresh_token=refresh_token,
        )
