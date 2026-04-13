from fastapi import HTTPException

from app.module.user.domain.ports.user_read_port import UserReadPort
from app.module.user.domain.ports.user_write_port import UserWritePort


class DeleteUserUseCase:
    def __init__(self, user_read_adapter: UserReadPort, user_write_adapter: UserWritePort):
        self.user_read_adapter = user_read_adapter
        self.user_write_adapter = user_write_adapter

    def execute(self, user_id: int) -> None:
        user = self.user_read_adapter.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.user_write_adapter.delete(user_id)