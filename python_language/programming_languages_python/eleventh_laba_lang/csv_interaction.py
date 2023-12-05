"""
Данный модуль предназначен для реализации логики взаимодействия с csv файлами относительно БД
"""
import csv


def db_to_csv(data: dict) -> None:
    """
    Функция, которая считывает данные из БД и записывает в csv.
    :data: словарь, взятый с 1 задания, который мы обрабатываем для сохранения.
    """
    with open('output.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Запись заголовков
        headers = ['teacher_id', 'name', 'age',
                   'position_id', 'position_title',
                   'department_id', 'department_title', 'institute']
        csv_writer.writerow(headers)

        # Запись данных
        for teacher_id, teacher_data in data.items():
            row = [
                teacher_id,
                teacher_data['name'],
                teacher_data['age'],
                teacher_data['position']['id'],
                teacher_data['position']['title'],
                teacher_data['department']['id'],
                teacher_data['department']['title'],
                teacher_data['department']['institute']
            ]
            csv_writer.writerow(row)


def csv_to_db() -> dict:
    data_dict = {}

    with open("output.csv", 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Пропуск заголовков

        for row in csv_reader:
            teacher_id, name, age, position_id, position_title, department_id, department_title, institute = row

            data_dict[teacher_id] = {
                'name': name,
                'age': age,
                'position': {'id': position_id, 'title': position_title},
                'department': {'id': department_id, 'title': department_title, 'institute': institute}
            }

    return data_dict
