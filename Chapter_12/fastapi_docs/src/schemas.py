from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class NoteBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)


class NoteModel(NoteBase):
    tags: List[int]


class NoteUpdate(NoteModel):
    done: bool


class NoteStatusUpdate(BaseModel):
    done: bool


class NoteResponse(NoteBase):
    id: int
    done: bool
    created_at: datetime | None
    updated_at: Optional[datetime] | None
    tags: List[TagResponse] | None

    model_config = ConfigDict(from_attributes=True)


# Схема користувача
class User(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    model_config = ConfigDict(from_attributes=True)


# Схема для запиту реєстрації
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# Схема для токену
class Token(BaseModel):
    access_token: str
    token_type: str


class RequestEmail(BaseModel):
    email: EmailStr
