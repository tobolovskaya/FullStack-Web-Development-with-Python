from sqlalchemy import event, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


# Створення базового класу
class Base(DeclarativeBase):
    pass


# Модель User
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)


# Обробник події перед вставкою
@event.listens_for(User, "before_insert")
def validate_user(mapper, connection, target):
    if len(target.username) < 3:
        raise ValueError("Username must be at least 3 characters long")
    if target.age < 18:
        raise ValueError("User must be at least 18 years old")


# Налаштування бази даних
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    # Спроба додати користувача з некоректними даними
    try:
        new_user = User(username="Jo", age=17)
        session.add(new_user)
        session.commit()
    except ValueError as e:
        print(f"Error: {e}")

    session.close()