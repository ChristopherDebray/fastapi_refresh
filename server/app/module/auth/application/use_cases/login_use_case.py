from fastapi import HTTPException, status

from app.core.security.encrypt_service import EncryptService
from app.core.security.jwt_service import JwtService
from app.module.auth.domain.ports.auth_read_port import AuthReadPort
from app.module.auth.infrastructure.dtos.inputs import LoginDto
from app.module.auth.infrastructure.dtos.outputs import AuthLoginResponseDto
from app.module.user.infrastructure.dtos.outputs import UserResponseDto


class LoginUseCase:
    def __init__(self, auth_read_repo: AuthReadPort) -> None:
        self.auth_read_repo = auth_read_repo

    def execute(self, dto: LoginDto) -> AuthLoginResponseDto:
        user = self.auth_read_repo.find_by_email(dto.email)
        if user is None or not EncryptService.verify(dto.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        token = JwtService.create_access_token(user.id, user.email, user.role)
        return AuthLoginResponseDto(
            user=UserResponseDto(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                role=user.role,
            ),
            access_token=token,
        )
