from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(120), unique=True)


engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)


if __name__ == '__main__':
    with Session(engine) as session:
        # Додавання об'єкта
        user = User(name='John Doe', email='john@example.com')
        session.add(user)
        session.commit()

        # Оновлення об'єкта
        user = session.get(User, 1)
        print(user.id, user.name, user.email)
        if user:
            user.name = 'John Smith'
            user.email = 'john.smith@example.com'
            session.commit()

        # Видалення об'єкта
        user = session.get(User, 1)
        print(user.id, user.name, user.email)
        if user:
            session.delete(user)
            session.commit()
