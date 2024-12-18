from sqlalchemy import create_engine, Integer, String
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


# Налаштування двигуна та сесії
engine = create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":

    try:
        # Початок транзакції
        with session.begin():
            new_user = User(username="Alice", age=25)
            session.add(new_user)
            # Виконуємо commit автоматично по завершенні контекстного менеджера
        print("Transaction committed successfully.")
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back. Error: {e}")
    finally:
        session.close()
