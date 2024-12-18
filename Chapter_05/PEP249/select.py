from sqlite3 import Error

from connect import create_connection, database


def select_projects(conn):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM projects;")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_all_tasks(conn):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_task_by_status(conn, status):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE status=?", (status,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


if __name__ == '__main__':
    with create_connection(database) as conn:
        print("Projects:")
        projects = select_projects(conn)
        print(projects)
        print("\nQuery all tasks")
        tasks = select_all_tasks(conn)
        print(tasks)
        print("\nQuery task by status:")
        task_by_priority = select_task_by_status(conn, True)
        print(task_by_priority)