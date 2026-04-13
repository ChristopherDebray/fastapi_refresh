from pydantic import BaseModel, ConfigDict

class UserResponseDto(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
