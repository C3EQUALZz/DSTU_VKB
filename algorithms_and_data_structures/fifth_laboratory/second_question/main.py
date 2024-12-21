import sys
from typing import Final, Dict

from algorithms_and_data_structures.fifth_laboratory.first_question.main import \
    main as fifth_laboratory_first_question_main
from algorithms_and_data_structures.first_laboratory.first_question.main import \
    main as first_laboratory_first_question_main
from algorithms_and_data_structures.first_laboratory.second_question.main import \
    main as first_laboratory_second_question_main
from algorithms_and_data_structures.fourth_laboratory.first_question.main import \
    main as fourth_laboratory_first_question_main
from algorithms_and_data_structures.fourth_laboratory.second_question.main import \
    main as fourth_laboratory_second_question_main
from algorithms_and_data_structures.second_laboratory.first_question.main import \
    main as second_laboratory_first_question_main
from algorithms_and_data_structures.second_laboratory.second_question.main import \
    main as second_laboratory_second_question_main
from algorithms_and_data_structures.second_laboratory.third_question.main import \
    main as second_laboratory_third_question_main
from algorithms_and_data_structures.third_laboratory.second_question.main import \
    main as third_laboratory_second_question_main
from algorithms_and_data_structures.third_laboratory.third_question.main import \
    main as third_laboratory_third_question_main

CHOICES: Final[Dict] = {
    "1": {
        "1": first_laboratory_first_question_main,
        "2": first_laboratory_second_question_main,
    },
    "2": {
        "1": second_laboratory_first_question_main,
        "2": second_laboratory_second_question_main,
        "3": second_laboratory_third_question_main,
    },
    "3": {
        "2": third_laboratory_second_question_main,
        "3": third_laboratory_third_question_main,
    },
    "4": {
        "1": fourth_laboratory_first_question_main,
        "2": fourth_laboratory_second_question_main
    },
    "5": {
        "1": fifth_laboratory_first_question_main
    }
}


def main() -> None:
    while True:
        number_of_laboratory = input("Введите номер лабораторной работы: ")

        if number_of_laboratory not in CHOICES:
            print("Нет такого номера лабораторной работы", file=sys.stderr)
            continue

        number_of_question = input("Введите номер задания для лабораторной работы: ")

        if CHOICES.get(number_of_laboratory).get(number_of_question) is None:
            print("Нет такого задания в данной лабораторной работе", file=sys.stderr)

        CHOICES[number_of_laboratory][number_of_question]()


if __name__ == '__main__':
    main()
