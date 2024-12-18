from sqlalchemy import create_engine, select, func
from models import User, Address

engine = create_engine("sqlite:///example.db")

if __name__ == "__main__":
    with engine.connect() as connection:
        # Вибірка всіх користувачів
        stmt = select(User)
        result = connection.execute(stmt)
        print("All users:")
        for row in result:
            print(f"<User(id={row.id}, name='{row.name}', age={row.age})>")

        # Фільтрація користувачів за віком
        stmt = select(User).where(User.age > 21)
        result = connection.execute(stmt)
        print("\nFiltered users (age > 21):")
        for row in result:
            print(f"<User(id={row.id}, name='{row.name}', age={row.age})>")

        # Сортування користувачів за іменем та обмеження результатів
        stmt = select(User).order_by(User.name).limit(2)
        result = connection.execute(stmt)
        print("\nSorted users (limited to 2):")
        for row in result:
            print(f"<User(id={row.id}, name='{row.name}', age={row.age})>")

        # JOIN користувачів та адрес
        stmt = select(User, Address).join(Address)
        result = connection.execute(stmt)
        print("\nUsers with addresses (JOIN):")
        for row in result:
            print(
                f"User: <User(id={row.id}, name='{row.name}', age={row.age})>, "
                f"Address: <Address(id={row[3]}, street='{row[4]}', city='{row[5]}')>"
            )

        # LEFT JOIN користувачів та адрес
        stmt = select(User, Address).join(Address, isouter=True)
        result = connection.execute(stmt)
        print("\nUsers with addresses (LEFT JOIN):")
        for row in result:
            address = (
                f"<Address(id={row[3]}, street='{row[4]}', city='{row[5]}')"
                if row[3]
                else None
            )
            print(
                f"User: <User(id={row.id}, name='{row.name}', age={row.age})>, Address: {address}>"
            )

        # FULL JOIN користувачів та адрес
        stmt = select(User, Address).outerjoin(Address, full=True)
        result = connection.execute(stmt)
        print("\nUsers with addresses (FULL JOIN):")
        for row in result:
            user = (
                f"<User(id={row.id}, name='{row.name}', age={row.age})>"
                if row.id
                else None
            )
            address = (
                f"<Address(id={row[3]}, street='{row[4]}', city='{row[5]}')"
                if row[3]
                else None
            )
            print(f"User: {user}, Address: {address}>")

        # Агрегація - підрахунок кількості користувачів
        stmt = select(func.count(User.id))
        result = connection.execute(stmt)
        count = result.scalar()
        print(f"\nTotal number of users: {count}")