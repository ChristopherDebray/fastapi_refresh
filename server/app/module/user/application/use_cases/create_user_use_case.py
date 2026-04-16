from app.core.security.encrypt_service import EncryptService
from app.module.user.domain.ports.user_write_port import UserWritePort
from app.module.user.infrastructure.dtos.inputs import UserCreateDto
from app.module.user.infrastructure.dtos.outputs import UserResponseDto


class CreateUserUseCase:
    def __init__(self, user_write_adapter: UserWritePort) -> None:
        self.user_write_adapter = user_write_adapter

    def execute(self, dto: UserCreateDto) -> UserResponseDto:
        dto.password = EncryptService.hash(dto.password)
        return self.user_write_adapter.save(dto)
