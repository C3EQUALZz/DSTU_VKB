from algorithms_and_data_structures.third_laboratory.third_question.calculator import \
    evaluate_rpn


def main() -> None:
    expression = input("Введите выражение в обратной польской записи: ")
    try:
        result = evaluate_rpn(expression)
        print("Результат:", result)
    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()
