from typing import Protocol

from app.module.user.infrastructure.dtos.outputs import UserResponseDto


class UserReadPort(Protocol):
    def find_all(self) -> list[UserResponseDto]: ...
    def find_by_id(self, user_id: int) -> UserResponseDto | None: ...
