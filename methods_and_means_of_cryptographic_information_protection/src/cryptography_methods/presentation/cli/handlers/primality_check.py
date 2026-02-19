import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.primality_check.check import (
    PrimalityCheckCommand,
    PrimalityCheckCommandHandler,
)
from cryptography_methods.application.commands.primality_check.find_in_interval import (
    FindPrimesInIntervalCommand,
    FindPrimesInIntervalCommandHandler,
)
from cryptography_methods.application.common.views.find_primes_in_interval import (
    FindPrimesInIntervalView,
    PrimeResultPerMethod,
)
from cryptography_methods.application.common.views.primality_check import (
    PrimalityCheckView,
)


@click.group(name="primality-check")
def primality_check_group() -> None:
    ...


@primality_check_group.command("check")
@click.option(
    "-n",
    "--number",
    required=True,
    help="Число для проверки на простоту",
    type=int,
)
@click.option(
    "-k",
    "--iterations",
    default=20,
    help="Количество итераций теста Миллера-Рабина",
    type=int,
)
def cmd_check_handler(
    number: int,
    iterations: int,
    interactor: FromDishka[PrimalityCheckCommandHandler],
) -> None:
    if number < 2:  # noqa: PLR2004
        click.echo("Число должно быть >= 2")
        return

    if iterations <= 0:
        click.echo("Количество итераций должно быть положительным")
        return

    command: PrimalityCheckCommand = PrimalityCheckCommand(
        number=number,
        iterations=iterations,
    )

    view: PrimalityCheckView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Проверка на простоту — тест Миллера-Рабина"
    table.field_names = ["число", "простое?", "итерации"]
    table.add_row([
        view.number,
        "Да" if view.is_prime else "Нет",
        view.iterations,
    ])

    click.echo(table)


def _render_histogram(
    histogram: dict[int, int],
    max_bar: int = 40,
) -> str:
    if not histogram:
        return ""
    max_count = max(histogram.values())
    scale = max_bar / max_count if max_count > 0 else 1
    lines: list[str] = []
    for gap, count in sorted(histogram.items()):
        bar_len = max(1, int(count * scale))
        bar = "#" * bar_len
        lines.append(f"  L = {gap:<3} | {bar} ({count})")
    return "\n".join(lines)


def _note_for(r: PrimeResultPerMethod) -> str:
    parts: list[str] = []
    if r.fermat and not r.miller_rabin:
        parts.append("Ферма ошибся")
    if r.trial_division and not r.miller_rabin:
        parts.append("пробные деления ошибся")
    if not r.trial_division and r.miller_rabin:
        parts.append("пробные деления не нашёл")
    if not r.fermat and r.miller_rabin:
        parts.append("Ферма не нашёл")
    return "; ".join(parts)


@primality_check_group.command("find-in-interval")
@click.option(
    "-s", "--start",
    default=1000,
    help="Начало интервала",
    type=int,
)
@click.option(
    "-e", "--end",
    default=1300,
    help="Конец интервала",
    type=int,
)
@click.option(
    "-tp", "--trial-primes",
    default=10,
    help="Количество простых для пробных делений (5-20)",
    type=click.IntRange(5, 20),
)
@click.option(
    "-fb", "--fermat-bases",
    default=2,
    help="Количество оснований теста Ферма (1-3)",
    type=click.IntRange(1, 3),
)
@click.option(
    "-k", "--miller-rabin-iterations",
    default=20,
    help="Количество итераций теста Миллера-Рабина",
    type=int,
)
def cmd_find_in_interval_handler(
    start: int,
    end: int,
    trial_primes: int,
    fermat_bases: int,
    miller_rabin_iterations: int,
    interactor: FromDishka[FindPrimesInIntervalCommandHandler],
) -> None:
    if start >= end:
        click.echo("Начало интервала должно быть меньше конца")
        return

    command = FindPrimesInIntervalCommand(
        start=start,
        end=end,
        num_trial_primes=trial_primes,
        num_fermat_bases=fermat_bases,
        miller_rabin_iterations=miller_rabin_iterations,
    )

    view: FindPrimesInIntervalView = asyncio.run(
        interactor(command),
    )

    # 1. Параметры
    params_table = PrettyTable()
    params_table.title = "Параметры поиска"
    params_table.field_names = ["Параметр", "Значение"]
    params_table.align["Параметр"] = "l"
    params_table.align["Значение"] = "r"
    params_table.add_rows([
        ["Интервал", f"({view.interval_start}, {view.interval_end})"],
        ["Простых для делений", view.num_trial_primes],
        ["Оснований Ферма", view.num_fermat_bases],
        ["Итераций М-Р", view.miller_rabin_iterations],
    ])
    click.echo(params_table)
    click.echo()

    # 2. Сравнение методов
    cmp_table = PrettyTable()
    cmp_table.title = "Сравнение методов"
    cmp_table.field_names = [
        "Число", "Проб. дел.", "Ферма", "М-Р", "Примечание",
    ]
    for r in view.results_per_number:
        yn = lambda v: "Да" if v else "Нет"  # noqa: E731
        cmp_table.add_row([
            r.number,
            yn(r.trial_division),
            yn(r.fermat),
            yn(r.miller_rabin),
            _note_for(r),
        ])
    click.echo(cmp_table)
    click.echo()

    # 3. Простые и разности
    primes_table = PrettyTable()
    primes_table.title = "Простые числа и разности L(i)"
    primes_table.field_names = ["i", "p(i)", "L(i)"]
    for i, p in enumerate(view.primes):
        gap_str = (
            str(view.gaps[i]) if i < len(view.gaps) else "—"
        )
        primes_table.add_row([i + 1, p, gap_str])
    click.echo(primes_table)
    click.echo()

    # 4. ASCII-гистограмма
    click.echo("Гистограмма разностей L(i):")
    click.echo(_render_histogram(view.histogram))
    click.echo()

    # 5. Статистика
    stats_table = PrettyTable()
    stats_table.title = "Статистика"
    stats_table.field_names = ["Показатель", "Значение"]
    stats_table.align["Показатель"] = "l"
    stats_table.align["Значение"] = "r"
    stats_table.add_rows([
        ["Количество простых", len(view.primes)],
        ["L(среднее)", f"{view.mean_gap:.4f}"],
        ["ln(x), x = середина", f"{view.ln_mid:.4f}"],
        [
            "|L(ср) - ln(x)|",
            f"{abs(view.mean_gap - view.ln_mid):.4f}",
        ],
    ])
    click.echo(stats_table)
