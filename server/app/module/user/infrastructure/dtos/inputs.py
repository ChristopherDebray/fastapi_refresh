from pydantic import BaseModel, ConfigDict

class UserCreateDto(BaseModel):
    email: str
    first_name: str
    last_name: str

class UserUpdateDto(BaseModel):
    id: int | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None