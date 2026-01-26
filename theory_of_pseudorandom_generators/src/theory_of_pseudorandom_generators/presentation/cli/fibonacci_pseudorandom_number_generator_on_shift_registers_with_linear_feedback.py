"""CLI commands for Fibonacci generator."""

import click
from dishka import FromDishka
from prettytable import PrettyTable

from theory_of_pseudorandom_generators.application.commands.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback import (
    FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommand,
    FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler,
)


@click.group(name="fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback")
def fibonacci_generator_group() -> None:
    """Fibonacci generator commands."""


@fibonacci_generator_group.command(name="generate")
@click.option(
    "-p",
    "--polynomial",
    required=True,
    help="Coefficients of primitive polynomial (space-separated)",
    type=str,
)
@click.option(
    "-s",
    "--start-state",
    required=True,
    help="Initial register state (space-separated)",
    type=str,
)
@click.option(
    "-k",
    "--shift",
    required=True,
    help="Shift value k",
    type=int,
)
@click.option(
    "-c",
    "--column-index",
    default=0,
    help="Column index",
    type=int,
)
def cmd_generate_handler(
    polynomial: str,
    start_state: str,
    shift: int,
    column_index: int,
    interactor: FromDishka[
        FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler
    ],
) -> None:
    """Generate Fibonacci sequence."""
    try:
        poly_coeffs = tuple(int(x) for x in polynomial.split())
        start_state_values = tuple(int(x) for x in start_state.split())

        command = FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommand(
            polynomial_coefficients=poly_coeffs,
            start_state=start_state_values,
            shift=shift,
            column_index=column_index,
        )

        view = interactor(command)
        
        # Формируем строку полинома
        poly_terms = []
        for i, c in enumerate(poly_coeffs):
            if c == 1:
                if i == 0:
                    poly_terms.append("1")
                elif i == 1:
                    poly_terms.append("x")
                else:
                    poly_terms.append(f"x^{i}")
        poly_str = " + ".join(poly_terms) if poly_terms else "0"
        
        # Отображение результатов с помощью PrettyTable
        print(f"\nГенератор Фибоначчи псевдослучайных чисел на регистрах сдвига с линейной обратной связью")
        print(f"Полином: P(x) = {poly_str}")
        print(f"\nПараметры:")
        params_table = PrettyTable(["Параметр", "Значение"])
        params_table.align = "l"
        params_table.add_row(["Степень многочлена (N)", str(len(start_state_values))])
        params_table.add_row(["Коэффициенты полинома", " ".join(str(c) for c in poly_coeffs)])
        params_table.add_row(["Начальное состояние", " ".join(str(s) for s in start_state_values)])
        params_table.add_row(["Сдвиг (k)", str(shift)])
        params_table.add_row(["Индекс колонки", str(column_index)])
        print(params_table)
        
        # Матрица T
        print(f"\nКвадратичная матрица порядка N (T):")
        t_table = PrettyTable([f"q{i+1}" for i in range(len(view.transition_matrix_t[0]))])
        t_table.align = "c"
        for row in view.transition_matrix_t:
            t_table.add_row(row)
        print(t_table)
        
        # Матрица V
        print(f"\nСопровождающая матрица V = T^{shift}:")
        v_table = PrettyTable([f"q{i+1}" for i in range(len(view.transition_matrix_v[0]))])
        v_table.align = "c"
        for row in view.transition_matrix_v:
            v_table.add_row(row)
        print(v_table)
        
        # Таблица состояний
        total_states = len(view.states_sequence)
        print(f"\nТаблица состояний (всего {total_states} состояний):")
        states_table = PrettyTable(["№"] + [f"q{i+1}" for i in range(len(start_state_values))])
        states_table.align = "c"
        for idx, state in enumerate(view.states_sequence, 1):
            states_table.add_row([idx] + list(state))
        print(states_table)
        
        # Двоичная последовательность
        binary_str = "".join(view.binary_sequence)
        print(f"\nДвоичная последовательность (выходные биты):")
        print(binary_str)
        
        # Десятичная последовательность
        print(f"\nДесятичные значения:")
        decimal_str = " ".join(str(d) for d in view.decimal_sequence)
        print(decimal_str)
        
        # Период
        print(f"\nПериод генератора: δ = {view.period}")
        print(f"Рассчитанный период: S = 2^N - 1 = 2^{len(start_state_values)} - 1 = {view.max_period}")
        
        # Проверка максимального периода
        print(f"\nНОД(S, k) = НОД({view.max_period}, {shift}) = {view.gcd_s_k}")
        if view.is_max_period:
            print("✓ Период максимальный (НОД(S, k) = 1)")
        else:
            print("✗ Период не максимальный (НОД(S, k) ≠ 1)")
        
    except ValueError as e:
        click.echo(f"Ошибка ввода: {e}", err=True)
    except Exception as e:
        click.echo(f"Ошибка: {e}", err=True)

