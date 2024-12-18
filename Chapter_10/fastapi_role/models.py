from enum import Enum

from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import DeclarativeBase

from database import engine


class Base(DeclarativeBase):
    pass


class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(SqlEnum(UserRole), default=UserRole.USER, nullable=False)


Base.metadata.create_all(bind=engine)
