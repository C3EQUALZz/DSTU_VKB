import click
from dishka import FromDishka
from prettytable import PrettyTable

from theory_of_pseudorandom_generators.application.commands.polynomial_congruent_pseudorandom_number_generator import (
    PolynomialCongruentPseudorandomNumberGeneratorCommand,
    PolynomialCongruentPseudorandomNumberGeneratorCommandHandler,
)


@click.group(name="polynomial_congruent_pseudorandom_number_generator")
def polynomial_congruent_pseudorandom_number_generator_group() -> None:
    ...


@polynomial_congruent_pseudorandom_number_generator_group.command(name="generate")
@click.option("-a1", required=True, help="a number for generate sequence", type=int)
@click.option("-a2", required=True, help="a number for generate sequence", type=int)
@click.option("-b", required=True, help="b number for generate sequence", type=int)
@click.option("-m", required=True, help="m number for generate sequence", type=int)
@click.option("-x0", required=True, help="x0 start number for generate sequence", type=int)
@click.option("-s", "--size", required=True, help="size of sequence", type=int, default=200)
def cmd_generate_handler(
        a1: int,
        a2: int,
        b: int,
        m: int,
        x0: int,
        size: int,
        interactor: FromDishka[PolynomialCongruentPseudorandomNumberGeneratorCommandHandler]
) -> None:
    command: PolynomialCongruentPseudorandomNumberGeneratorCommand = PolynomialCongruentPseudorandomNumberGeneratorCommand(
        a1=a1,
        a2=a2,
        b=b,
        m=m,
        x0=x0,
        size=size,
    )

    view = interactor(command)
    
    # Отображение результатов с помощью PrettyTable
    print(f"\nПолиномиальный конгруэнтный генератор псевдослучайных чисел {m} {a1} {a2} {b} {x0}")
    print(f"Формула: Xn+1 = (a2 * Xn² + a1 * Xn + b) mod m")
    print(f"\nВведенные параметры:")
    params_table = PrettyTable(["Параметр", "Значение"])
    params_table.align = "l"
    params_table.add_row(["m (m > 0)", str(m)])
    params_table.add_row(["a1 (целое число)", str(a1)])
    params_table.add_row(["a2 (целое число)", str(a2)])
    params_table.add_row(["b (0 ≤ b ≤ m)", str(b)])
    params_table.add_row(["x0 (0 ≤ x0 ≤ m)", str(x0)])
    print(params_table)
    
    print(f"\nПроверка условий для максимального периода:")
    conditions_table = PrettyTable(["Условие", "Описание", "Статус", "Детали"])
    conditions_table.align = "l"
    
    for condition in view.conditions:
        if condition.condition_number == 0:
            continue  # Пропускаем базовые проверки
        status = "выполнено" if condition.is_fulfilled else "не выполнено"
        # Форматируем детали: если условие выполнено, добавляем "выполнено: " в начало
        details = condition.details
        if condition.is_fulfilled and not details.startswith("выполнено"):
            details = f"выполнено: {details}"
        conditions_table.add_row([
            f"Условие {condition.condition_number}",
            condition.description,
            status,
            details
        ])
    
    print(conditions_table)
    
    # Итоговый результат
    if view.is_max_period:
        print("\n✓ Все условия для максимального периода выполнены.")
    else:
        print("\n✗ Условия для максимального периода не выполнены.")
    
    print(f"\nДлина периода: {view.period}")
    if view.period == view.m:
        print(f"✓ Период максимальный (равен m = {view.m})")
    else:
        print(f"Период меньше максимального (m = {view.m})")
