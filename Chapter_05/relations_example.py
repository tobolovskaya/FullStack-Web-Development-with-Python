from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import (
    relationship,
    sessionmaker,
    DeclarativeBase,
    mapped_column,
    Mapped,
)

# Створення підключення до бази даних
engine = create_engine("sqlite:///example_relation.db")
Session = sessionmaker(bind=engine)
session = Session()


# Створення базового класу для декларативних моделей
class Base(DeclarativeBase):
    pass


# Визначення таблиці асоціацій
association_table = Table(
    "association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("group_id", Integer, ForeignKey("groups.id", ondelete="CASCADE")),
    PrimaryKeyConstraint("user_id", "group_id"),
)


# Визначення моделі User
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    groups: Mapped[list["Group"]] = relationship(
        "Group",
        secondary=association_table,
        back_populates="users",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name='{self.name}')>"


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    users: Mapped[list["User"]] = relationship(
        "User",
        secondary=association_table,
        back_populates="groups",
    )

    def __repr__(self) -> str:
        return f"<Group(id={self.id}, name='{self.name}')>"


# Створення таблиць у базі даних
Base.metadata.create_all(engine)

if __name__ == "__main__":
    # Створення об'єктів User та Group
    user1 = User(name="John")
    user2 = User(name="Jane")
    group1 = Group(name="Group A1")
    group2 = Group(name="Group A2")

    # Додавання користувачів до груп
    user1.groups.extend([group1, group2])
    user2.groups.append(group2)

    # Додавання об'єктів до сесії та збереження змін
    session.add_all([user1, user2, group1, group2])
    session.commit()

    # Запити до бази даних
    print("Користувачі:")
    users = session.query(User).all()
    for user in users:
        print(user)
        print("Групи користувача:")
        for group in user.groups:
            print(group)
        print()

    print("Групи:")
    groups = session.query(Group).all()
    for group in groups:
        print(group)
        print("Користувачі групи:")
        for user in group.users:
            print(user)
        print()

    # Закриття сесії
    session.close()
