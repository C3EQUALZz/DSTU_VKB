import sqlite3


class Database:
    inheritance = None

    def __new__(cls, database_name):
        if Database.inheritance is None:
            Database.inheritance = sqlite3.connect(database_name)
        return Database.inheritance

    def __enter__(self):
        return Database.inheritance

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            Database.inheritance.rollback()
        else:
            Database.inheritance.commit()
        Database.inheritance.close()


# with Database("/home/c3equalz/Databases/tuple") as db:
#     cursor = db.cursor()
#     cursor.executescript("""
#         INSERT INTO tuple
#         values (4, 'Artem', 'Ushenin', 'Vitalevich', 19)
#     """)
#     cursor.execute("SELECT * FROM tuple")
#     result = cursor.fetchall()
#     print(result)
