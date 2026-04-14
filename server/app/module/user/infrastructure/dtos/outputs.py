from pydantic import BaseModel, ConfigDict


class UserResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    first_name: str
    last_name: str
