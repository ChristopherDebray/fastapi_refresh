from fastapi import HTTPException

from app.module.user.domain.ports.user_read_port import UserReadPort
from app.module.user.domain.ports.user_write_port import UserWritePort
from app.module.user.infrastructure.dtos.inputs import UserUpdateDto


class UpdateUserUseCase:
    def __init__(
            self,
            user_write_adapter: UserWritePort,
            user_read_adapter: UserReadPort
        ):
        self.user_write_adapter = user_write_adapter
        self.user_read_adapter = user_read_adapter
    
    def execute(self, id: int, dto: UserUpdateDto):
        user = self.user_read_adapter.find_by_id(id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_update_dto = UserUpdateDto(
            id=id,
            email=dto.email,
            first_name=dto.first_name,
            last_name=dto.last_name,
        )
        return self.user_write_adapter.update(user_update_dto)