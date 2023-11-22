from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from db_creation.tables import Position, Department, Teacher

engine = create_engine('sqlite:///database.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Проверяем содержимое таблицы Position
positions = session.query(Position).all()
print("Positions:")
for position in positions:
    print(position.id, position.title)

# Проверяем содержимое таблицы Department
departments = session.query(Department).all()
print("\nDepartments:")
for department in departments:
    print(department.id, department.title, department.institute)

# Проверяем содержимое таблицы Teacher
teachers = session.query(Teacher).all()
print("\nTeachers:")
for teacher in teachers:
    print(teacher.id, teacher.name, teacher.age, teacher.department_id, teacher.position_id)
