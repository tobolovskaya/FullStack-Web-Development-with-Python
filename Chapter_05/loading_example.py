from typing import List
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, Session, joinedload

engine = create_engine("sqlite:///example_ex.db", echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    posts: Mapped[List["Post"]] = relationship(back_populates="user")


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")


Base.metadata.create_all(engine)

# Додавання користувачів та їхніх постів
with Session(engine) as session:
    user1 = User(name="Аліса")
    post1 = Post(title="Перший пост Аліси", user=user1)
    post2 = Post(title="Другий пост Аліси", user=user1)
    session.add_all([user1, post1, post2])
    session.commit()

# Демонстрація Lazy Loading
with Session(engine) as session:
    stmt = select(User).where(User.name == "Аліса")
    user = session.scalars(stmt).first()
    print(f"Користувач: {user.name}")

    # Тут буде виконано додатковий запит
    print("Пости користувача:")
    for post in user.posts:
        print(f"- {post.title}")

# Демонстрація Joined Loading
with Session(engine) as session:
    stmt = select(User).where(User.name == "Аліса").options(joinedload(User.posts))
    user = session.scalars(stmt).first()
    print(f"Користувач: {user.name}")

    # Тут буде виконано додатковий запит
    print("Пости користувача:")
    for post in user.posts:
        print(f"- {post.title}")