"""
Задача №49. Списки по классам

Формат входных данных

В каждой строке сначала записан номер класса (число, равное 9, 10 или 11), затем (через пробел) – фамилия ученика.
Общее число строк в файле не превосходит 100000. Длина каждой фамилии не превосходит 50 символов.

Формат выходных данных

Необходимо вывести список школьников по классам: сначала всех учеников 9 класса, затем – 10, затем – 11.
Внутри одного класса порядок вывода фамилий должен быть таким же, как на входе.
"""
from typing import Dict, List


def read_students(file_path: str) -> Dict[int, List[str]]:
    # Словарь для хранения учеников по классам
    classes: Dict[int, List[str]] = {9: [], 10: [], 11: []}

    # Чтение данных из файла
    with open(file_path, 'r', encoding='KOI8-r') as file:
        for line in file:
            # Разделяем строку на номер класса и фамилию
            class_number, surname = line.strip().split(maxsplit=1)
            class_number = int(class_number)  # Преобразуем номер класса в целое число

            # Добавляем фамилию в соответствующий класс
            if class_number in classes:
                classes[class_number].append(f"{class_number} {surname}")

    return classes


def write_students(classes: Dict[int, List[str]], output_path: str) -> None:
    # Запись учеников в файл
    with open(output_path, 'w', encoding='KOI8-r') as file:
        for class_number in range(9, 12):  # Проходим по классам 9, 10, 11
            for student in classes[class_number]:
                file.write(student + '\n')


def main() -> None:
    input_file_path = "input.txt"
    output_file_path = "output.txt"
    students_by_class = read_students(input_file_path)
    write_students(students_by_class, output_file_path)


if __name__ == '__main__':
    main()
