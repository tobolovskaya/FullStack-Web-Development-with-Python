from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import User, Address, Base

engine = create_engine("sqlite:///example.db")
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":

    # Вибірка всіх користувачів
    users = session.query(User).all()
    print("All users:")
    for user in users:
        print(user)

    # Фільтрація користувачів за віком
    filtered_users = session.query(User).filter(User.age > 21).all()
    print("\nFiltered users (age > 18):")
    for user in filtered_users:
        print(user)

    # Сортування користувачів за іменем та обмеження результатів
    sorted_users = session.query(User).order_by(User.name).limit(2).all()
    print("\nSorted users (limited to 5):")
    for user in sorted_users:
        print(user)

    # JOIN користувачів та адрес
    results = (
        session.query(User, Address).join(Address, User.id == Address.user_id).all()
    )
    print("\nUsers with addresses (JOIN):")
    for user, address in results:
        print(f"User: {user}, Address: {address}")

    # LEFT JOIN користувачів та адрес
    results = (
        session.query(User, Address)
        .join(Address, User.id == Address.user_id, isouter=True)
        .all()
    )
    print("\nUsers with addresses (LEFT JOIN):")
    for user, address in results:
        print(f"User: {user}, Address: {address}")

    # FULL JOIN користувачів та адрес
    result = session.query(User, Address).outerjoin(Address, full=True).all()
    print("\nUsers with addresses (FULL JOIN):")
    for user, address in result:
        print(f"User: {user}, Address: {address}")

    # Агрегація - підрахунок кількості користувачів
    count = session.query(func.count(User.id)).scalar()
    print(f"\nTotal number of users: {count}")

    session.close()