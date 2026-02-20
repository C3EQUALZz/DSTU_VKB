import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.primality_check.check import (
    PrimalityCheckCommand,
    PrimalityCheckCommandHandler,
)
from cryptography_methods.application.commands.primality_check.carmichael import (
    FindCarmichaelCommand,
    FindCarmichaelCommandHandler,
)
from cryptography_methods.application.commands.primality_check.find_in_interval import (
    FindPrimesInIntervalCommand,
    FindPrimesInIntervalCommandHandler,
)
from cryptography_methods.application.commands.primality_check.sieve_eratosthenes import (
    SieveEratosthenesCommand,
    SieveEratosthenesCommandHandler,
)
from cryptography_methods.application.common.views.find_primes_in_interval import (
    FindPrimesInIntervalView,
    PrimeResultPerMethod,
)
from cryptography_methods.application.common.views.carmichael import (
    FindCarmichaelView,
)
from cryptography_methods.application.common.views.primality_check import (
    PrimalityCheckView,
)
from cryptography_methods.application.common.views.sieve_eratosthenes import (
    SieveEratosthenesView,
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


@primality_check_group.command("sieve")
@click.option(
    "-s", "--start",
    default=500,
    help="Начало интервала",
    type=int,
)
@click.option(
    "-e", "--end",
    default=700,
    help="Конец интервала",
    type=int,
)
@click.option(
    "-mk", "--max-k",
    default=10,
    help="Максимальное k (1-20)",
    type=click.IntRange(1, 20),
)
def cmd_sieve_handler(
    start: int,
    end: int,
    max_k: int,
    interactor: FromDishka[SieveEratosthenesCommandHandler],
) -> None:
    if start >= end:
        click.echo("Начало интервала должно быть меньше конца")
        return

    command = SieveEratosthenesCommand(
        start=start,
        end=end,
        max_k=max_k,
    )

    view: SieveEratosthenesView = asyncio.run(
        interactor(command),
    )

    # 1. Параметры
    params_table = PrettyTable()
    params_table.title = "Параметры решета Эратосфена"
    params_table.field_names = ["Параметр", "Значение"]
    params_table.align["Параметр"] = "l"
    params_table.align["Значение"] = "r"
    params_table.add_rows([
        [
            "Интервал",
            f"({view.interval_start}, {view.interval_end})",
        ],
        ["Максимальное k", max_k],
    ])
    click.echo(params_table)
    click.echo()

    # 2. Таблица результатов
    results_table = PrettyTable()
    results_table.title = "Результаты решета"
    results_table.field_names = [
        "k", "Простые", "Прошло", "Всего", "Доля",
    ]
    results_table.align["Простые"] = "l"
    results_table.align["Доля"] = "r"
    for row in view.rows:
        primes_str = ",".join(str(p) for p in row.primes_used)
        results_table.add_row([
            row.k,
            primes_str,
            row.passing_count,
            row.total_count,
            f"{row.relative_count:.4f}",
        ])
    click.echo(results_table)
    click.echo()

    # 3. ASCII-график
    click.echo("График относительного количества:")
    max_bar = 40
    for row in view.rows:
        primes_str = ",".join(str(p) for p in row.primes_used)
        label = f"k = {row.k:<2} ({primes_str})"
        bar_len = max(1, int(row.relative_count * max_bar))
        bar = "#" * bar_len
        click.echo(
            f"  {label:<30} | {bar} "
            f"({row.relative_count:.4f})",
        )


@primality_check_group.command("carmichael")
@click.option(
    "-s", "--start",
    default=1,
    help="Начало интервала",
    type=int,
)
@click.option(
    "-e", "--end",
    default=10000,
    help="Конец интервала",
    type=int,
)
def cmd_carmichael_handler(
    start: int,
    end: int,
    interactor: FromDishka[FindCarmichaelCommandHandler],
) -> None:
    if start >= end:
        click.echo("Начало интервала должно быть меньше конца")
        return

    command = FindCarmichaelCommand(start=start, end=end)

    view: FindCarmichaelView = asyncio.run(
        interactor(command),
    )

    # 1. Параметры
    params_table = PrettyTable()
    params_table.title = "Поиск чисел Кармайкла"
    params_table.field_names = ["Параметр", "Значение"]
    params_table.align["Параметр"] = "l"
    params_table.align["Значение"] = "r"
    params_table.add_rows([
        [
            "Интервал",
            f"({view.interval_start}, {view.interval_end})",
        ],
        ["Проверено чисел", view.total_checked],
        ["Найдено", len(view.carmichael_numbers)],
    ])
    click.echo(params_table)
    click.echo()

    if not view.carmichael_numbers:
        click.echo("Числа Кармайкла не найдены.")
        return

    # 2. Таблица результатов
    results_table = PrettyTable()
    results_table.title = "Числа Кармайкла"
    results_table.field_names = [
        "Число", "Разложение", "Ферма (5 осн.)",
    ]
    results_table.align["Число"] = "r"
    results_table.align["Разложение"] = "l"
    for c in view.carmichael_numbers:
        factored = " x ".join(str(p) for p in c.prime_factors)
        results_table.add_row([
            c.number,
            factored,
            "Да" if c.passes_fermat else "Нет",
        ])
    click.echo(results_table)
