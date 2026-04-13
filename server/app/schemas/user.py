from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)