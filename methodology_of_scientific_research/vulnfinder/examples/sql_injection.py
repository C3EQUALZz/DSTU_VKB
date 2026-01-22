import sqlite3


def find_user_by_name(user_name: str) -> list[tuple[int, str]]:
    connection = sqlite3.connect("app.db")
    cursor = connection.cursor()

    query = f"SELECT id, name FROM users WHERE name = '{user_name}'"
    cursor.execute(query)
    rows = cursor.fetchall()

    connection.close()
    return rows

