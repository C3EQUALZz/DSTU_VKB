import click
from dishka import FromDishka
from prettytable import PrettyTable

from mathematical_algorithms_of_geometry_in_cryptography.application.commands.miller_rabit_test import (
    MakeMillerRabinTestCommand,
    MakeMillerRabitTestCommandHandler,
)
from mathematical_algorithms_of_geometry_in_cryptography.application.views.miller_rabin_test_view import (
    MillerRabinTestView,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.entities.miller_rabin_test import (
    MillerRabinTest,
)


@click.group(name="miller-rabin")
def miller_rabin_test_group() -> None:
    """Группа команд для теста Миллера-Рабина."""
    ...


def _convert_test_to_view(test: MillerRabinTest) -> MillerRabinTestView:
    """Преобразовать MillerRabinTest в View."""
    results_data = []
    for result in test.results:
        result_dict = {
            "iteration": result.iteration,
            "status": result.status.value,
            "s": result.parameters.s,
            "t": result.parameters.t,
            "a": result.parameters.a,
            "intermediate_values": result.intermediate_values,
        }
        results_data.append(result_dict)

    return MillerRabinTestView(
        number=int(test.number),
        iterations_count=test.iterations_count,
        is_complete=test.is_complete,
        is_probably_prime=test.is_probably_prime,
        is_composite=test.is_composite,
        results=tuple(results_data),
    )


@miller_rabin_test_group.command(name="test")
@click.option(
    "-n",
    "--number",
    required=True,
    help="Число для проверки на простоту",
    type=int,
)
@click.option(
    "-i",
    "--iterations",
    default=5,
    help="Количество итераций теста (по умолчанию: 5)",
    type=int,
)
@click.option(
    "-s",
    "--seed",
    default=None,
    help="Seed для генератора случайных чисел (опционально)",
    type=int,
)
def cmd_test_handler(
    number: int,
    iterations: int,
    seed: int | None,
    interactor: FromDishka[MakeMillerRabitTestCommandHandler],
) -> None:
    """Выполнить тест Миллера-Рабина для проверки числа на простоту."""
    # Валидация входных параметров
    if number <= 5:
        click.echo("Число должно быть больше 5", err=True)
        return

    if number % 2 == 0:
        click.echo("Число должно быть нечетным", err=True)
        return

    if iterations < 1:
        click.echo("Количество итераций должно быть положительным", err=True)
        return

    # Создаем команду
    command: MakeMillerRabinTestCommand = MakeMillerRabinTestCommand(
        number=number,
        iterations=iterations,
        random_seed=seed,
    )

    # Выполняем команду
    test: MillerRabinTest = interactor(command)

    # Преобразуем в View
    view: MillerRabinTestView = _convert_test_to_view(test)

    # Выводим основную таблицу с результатами
    main_table: PrettyTable = PrettyTable()
    main_table.title = "Результат теста Миллера-Рабина"
    main_table.field_names = [
        "Число",
        "Итераций выполнено",
        "Завершен",
        "Вероятно простое",
        "Составное",
    ]
    main_table.add_row(
        [
            view.number,
            view.iterations_count,
            "Да" if view.is_complete else "Нет",
            "Да" if view.is_probably_prime else "Нет",
            "Да" if view.is_composite else "Нет",
        ],
    )

    click.echo(main_table)

    # Выводим детальную таблицу для каждой итерации
    if view.results:
        click.echo("\nДетальные результаты итераций:")
        for result in view.results:
            iteration_table: PrettyTable = PrettyTable()
            iteration_table.title = f"Итерация {result['iteration']}"
            iteration_table.field_names = ["Параметр", "Значение"]
            iteration_table.add_row(["Статус", result["status"]])
            iteration_table.add_row(["s", result["s"]])
            iteration_table.add_row(["t", result["t"]])
            iteration_table.add_row(["a", result["a"]])

            # Добавляем промежуточные значения
            for key, value in result["intermediate_values"].items():
                iteration_table.add_row([key, value])

            click.echo(iteration_table)
