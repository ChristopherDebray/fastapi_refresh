from pydantic import BaseModel, EmailStr, Field


class UserCreateDto(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=55)
    last_name: str = Field(min_length=1, max_length=55)
    password: str = Field(min_length=6, max_length=55)


class UserUpdateDto(BaseModel):
    id: int | None = None
    email: EmailStr | None = None
    first_name: str | None = Field(default=None, min_length=1, max_length=55)
    last_name: str | None = Field(default=None, min_length=1, max_length=55)
