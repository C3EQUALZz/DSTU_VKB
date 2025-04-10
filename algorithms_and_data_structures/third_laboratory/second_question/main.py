from algorithms_and_data_structures.third_laboratory.second_question.bracket import \
    is_balanced


def main() -> None:
    user_data = input("Введите скобочную последовательность: ")

    print(
        f"{('Не является', 'Является')[is_balanced(user_data)]} скобочной последовательностью"
    )


if __name__ == "__main__":
    main()
