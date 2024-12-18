import pytest

import db

data = ("John", "john@example.com")


@pytest.fixture
def db_connection():
    with db.create_connection() as connection:
        yield connection


def test_db_operation(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            fullname STRING,
            email STRING
        );
    """)
    cursor.execute("INSERT INTO users (fullname, email) VALUES (?, ?)", data)
    db_connection.commit()
    r = cursor.execute("SELECT fullname, email FROM users")
    assert r.fetchone() == data
