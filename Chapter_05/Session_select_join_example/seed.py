from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Address

engine = create_engine("sqlite:///example.db")
Base.metadata.create_all(engine)  # Створення таблиць в базі даних

Session = sessionmaker(bind=engine)
session = Session()

# Створення користувачів
user1 = User(name="Пилип Перебийніс", age=25)
user2 = User(name="Микола Кожум'яка", age=30)
user3 = User(name="Ірина Сидоренко", age=20)

# Створення адрес
address1 = Address(street="вул. Саксаганського, 57", city="Київ", user=user1)
address2 = Address(street="вул. Соборності, 45", city="Полтава", user=user2)
address3 = Address(street="вул. Сумська, 61", city="Харків", user=user2)

# Додавання об'єктів до сесії
session.add_all([user1, user2, user3, address1, address2, address3])

# Збереження змін в базі даних
session.commit()

print("Database populated successfully.")

session.close()