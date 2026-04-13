from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str

class UserCreate(BaseModel):
    email: str
    first_name: str
    last_name: str

class UserUpdate(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None