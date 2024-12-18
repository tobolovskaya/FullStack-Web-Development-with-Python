from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    validates,
    sessionmaker,
)


# Створення базового класу
class Base(DeclarativeBase):
    pass


# Модель User
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    @validates("username")
    def validate_username(self, key, username: str) -> str:
        if not username:
            raise ValueError(f"Field {key} cannot be empty")
        if len(username) < 3:
            raise ValueError(f"Field '{key}' must be at least 3 characters long")
        return username

    @validates("age")
    def validate_age(self, key, age: int) -> int:
        if age < 18:
            raise ValueError("User must be at least 18 years old")
        return age


# Налаштування бази даних
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    # Використання
    try:
        new_user = User(username="Jo", age=17)
        session.add(new_user)
        session.commit()
    except ValueError as e:
        print(f"Error: {e}")

    session.close()