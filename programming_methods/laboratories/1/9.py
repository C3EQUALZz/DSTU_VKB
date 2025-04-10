"""
Задача №49. Списки по классам

Формат входных данных

В каждой строке сначала записан номер класса (число, равное 9, 10 или 11), затем (через пробел) – фамилия ученика.
Общее число строк в файле не превосходит 100000. Длина каждой фамилии не превосходит 50 символов.

Формат выходных данных

Необходимо вывести список школьников по классам: сначала всех учеников 9 класса, затем – 10, затем – 11.
Внутри одного класса порядок вывода фамилий должен быть таким же, как на входе.
"""

from typing import Dict, Iterable, List


def process_students(students: Iterable[str]) -> str:
    """
    Из условия задачи известно, что у нас всего 3 класса, поэтому заранее создал словарь с готовыми ключами.
    Здесь мы принимаем строку, и добавляем по нужному ключу в словарь.
    :param students: Итерируемый объект, который содержит данные о студентах в виде строк.
    :returns: Тот же самый вид строки, как было и в условии.
    """
    classes: Dict[int, List[str]] = {9: [], 10: [], 11: []}

    for student in students:
        class_number, surname = student.split()
        class_number = int(class_number)
        classes[class_number].append(f"{class_number} {surname}")

    result = ""
    for class_number in classes:
        result += "\n".join(student for student in classes[class_number]) + "\n"

    return result


def main() -> None:
    input_file_path = "input.txt"
    output_file_path = "output.txt"

    with open(input_file_path, "r", encoding="KOI8-r") as file:
        students_by_class = process_students(map(str.strip, file.readlines()))

    with open(output_file_path, "w", encoding="KOI8-r") as file:
        file.write(students_by_class)


if __name__ == "__main__":
    main()
