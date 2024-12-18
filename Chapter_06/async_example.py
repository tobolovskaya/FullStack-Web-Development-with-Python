import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, select


# Створення базового класу
class Base(DeclarativeBase):
    pass


# Модель User
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)


# Асинхронний двигун
async def async_main():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Створення асинхронної сесії
    async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with async_session() as session:
        # Додавання нового користувача
        new_user = User(username="Alice", age=25)
        session.add(new_user)
        await session.commit()

        # Запит користувачів
        result = await session.execute(select(User))
        users = result.scalars().all()
        for user in users:
            print(f"User: {user.username}, Age: {user.age}")


if __name__ == "__main__":
    # Запуск асинхронної функції
    asyncio.run(async_main())