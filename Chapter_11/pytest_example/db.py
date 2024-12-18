import sqlite3
from contextlib import contextmanager


@contextmanager
def create_connection():
    conn = sqlite3.connect(':memory:')
    yield conn
    conn.rollback()
    conn.close()
