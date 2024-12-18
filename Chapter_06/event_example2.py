from sqlalchemy import create_engine, Integer, String, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)


# Обробник події перед вставкою
@event.listens_for(User, "before_insert")
def before_insert_listener(mapper, connection, target):
    print(f"Before insert: {target.username}")


# Обробник події перед оновленням
@event.listens_for(User, "before_update")
def before_update_listener(mapper, connection, target):
    print(f"Before update: {target.username}")


# Налаштування бази даних
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":

    # Операція, яка тригерить події
    new_user = User(username="Charlie", age=22)
    session.add(new_user)
    session.commit()

    # Операція масового додавання, яка НЕ тригерить події
    session.bulk_insert_mappings(
        User, [{"username": "Alice", "age": 25}, {"username": "Bob", "age": 30}]
    )
    session.commit()

    # Операція, яка тригерить події для оновлення
    new_user.username = "Victoria"
    session.commit()

    session.close()