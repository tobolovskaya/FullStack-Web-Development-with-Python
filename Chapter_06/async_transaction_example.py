import asyncio

from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Створення базового класу
class Base(DeclarativeBase):
    pass


# Модель User
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)


# Асинхронний двигун і сесія
async def async_main():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with async_session() as session:
        try:
            async with session.begin():
                new_user = User(username="Alice", age=25)
                session.add(new_user)
                # Виконуємо commit автоматично по завершенні контекстного менеджера
            print("Transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            print(f"Transaction failed, rolled back. Error: {e}")


if __name__ == "__main__":
    asyncio.run(async_main())