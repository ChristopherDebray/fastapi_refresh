from app.module.user.domain.ports.user_read_port import UserReadPort
from app.module.user.infrastructure.dtos.outputs import UserResponseDto


class GetUsersUseCase:
    def __init__(self, user_read_adapter: UserReadPort):
        self.user_read_adapter = user_read_adapter

    def execute(self) -> list[UserResponseDto]:
        return self.user_read_adapter.find_all()
