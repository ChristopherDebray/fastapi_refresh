from app.module.user.domain.ports.user_read_port import UserReadPort
from app.module.user.infrastructure.dtos.outputs import UserResponseDto


class GetUserUseCase:
    def __init__(self, user_read_adapter: UserReadPort):
        self.user_read_adapter = user_read_adapter

    def execute(self, user_id: int) -> UserResponseDto | None:
        return self.user_read_adapter.find_by_id(user_id)