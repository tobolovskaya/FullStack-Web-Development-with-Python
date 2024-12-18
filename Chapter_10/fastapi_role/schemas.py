from pydantic import BaseModel, ConfigDict
from models import UserRole


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole


class UserModel(BaseModel):
    id: int
    username: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
