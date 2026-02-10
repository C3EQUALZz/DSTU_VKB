"""CLI handlers для протокола идентификации с нулевой передачей данных."""
import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.zero_knowledge_proof.execute import (
    ExecuteZeroKnowledgeProofCommand,
    ExecuteZeroKnowledgeProofCommandHandler
)
from cryptography_methods.application.commands.zero_knowledge_proof.execute_parallel import (
    ExecuteParallelZeroKnowledgeProofCommand,
    ExecuteParallelZeroKnowledgeProofCommandHandler
)
from cryptography_methods.application.common.views.zero_knowledge_proof import (
    ZeroKnowledgeProofExecutionView,
    ParallelZeroKnowledgeProofExecutionView,
)


@click.group(name="zero-knowledge-proof")
def zero_knowledge_proof_group() -> None:
    """Zero-Knowledge Proof protocol commands."""
    ...


@zero_knowledge_proof_group.command("execute")
@click.option(
    "-i",
    "--iterations",
    required=True,
    help="Number of protocol iterations",
    type=int
)
@click.option(
    "-b",
    "--bit-length",
    default=7,
    help="Bit length for prime numbers (default: 7, for two-digit primes)",
    type=int
)
@click.option(
    "--test-failure",
    is_flag=True,
    help="Test authentication failure by using wrong secret key",
    default=False
)
def cmd_execute_handler(
    iterations: int,
    bit_length: int,
    test_failure: bool,
    interactor: FromDishka[ExecuteZeroKnowledgeProofCommandHandler]
) -> None:
    if iterations <= 0:
        click.echo("Ошибка: количество итераций должно быть положительным числом")
        return

    if bit_length < 4:
        click.echo("Ошибка: bit_length должен быть не менее 4")
        return

    command: ExecuteZeroKnowledgeProofCommand = ExecuteZeroKnowledgeProofCommand(
        iterations=iterations,
        bit_length=bit_length,
        test_failure=test_failure,
    )

    try:
        view: ZeroKnowledgeProofExecutionView = asyncio.run(interactor(command))

        # Итоговая таблица
        table: PrettyTable = PrettyTable()
        table.title = "Zero-Knowledge Proof Protocol Results"
        table.field_names = ["Итерация", "r", "x", "b", "y", "Результат"]
        table.align = "l"

        for res in view.iterations:
            r_str = _truncate_number(str(res["r"]))
            x_str = _truncate_number(str(res["x"]))
            y_str = _truncate_number(str(res["y"])) if res["y"] is not None else "—"
            passed = "✓" if res["verification_passed"] else "✗"

            table.add_row([res["iteration"], r_str, x_str, res["b"], y_str, passed])

        click.echo(table)

    except Exception as e:
        click.echo(f"Ошибка при выполнении протокола: {e}")


@zero_knowledge_proof_group.command("parallel")
@click.option(
    "-t",
    "--iterations",
    required=True,
    help="Number of protocol iterations (t)",
    type=int
)
@click.option(
    "-k",
    "--key-count",
    default=5,
    help="Number of key pairs K (default: 5)",
    type=int
)
@click.option(
    "-b",
    "--bit-length",
    default=7,
    help="Bit length for prime numbers (default: 7, for two-digit primes)",
    type=int
)
@click.option(
    "--test-failure",
    is_flag=True,
    help="Test authentication failure by using wrong secret keys",
    default=False
)
def cmd_parallel_execute_handler(
    iterations: int,
    key_count: int,
    bit_length: int,
    test_failure: bool,
    interactor: FromDishka[ExecuteParallelZeroKnowledgeProofCommandHandler]
) -> None:
    if iterations <= 0:
        click.echo("Ошибка: количество итераций должно быть положительным числом")
        return

    if key_count <= 0:
        click.echo("Ошибка: количество ключей K должно быть положительным числом")
        return

    if bit_length < 4:
        click.echo("Ошибка: bit_length должен быть не менее 4")
        return

    command: ExecuteParallelZeroKnowledgeProofCommand = ExecuteParallelZeroKnowledgeProofCommand(
        iterations=iterations,
        bit_length=bit_length,
        k=key_count,
        test_failure=test_failure,
    )

    try:
        view: ParallelZeroKnowledgeProofExecutionView = asyncio.run(interactor(command))

        # Итоговая таблица
        table: PrettyTable = PrettyTable()
        table.title = f"Parallel ZKP Protocol (K={view.k}, t={view.total_iterations})"
        table.field_names = ["Итерация", "r", "x", "Биты (b1..bK)", "y", "Результат"]
        table.align = "l"

        for res in view.iterations:
            r_str = _truncate_number(str(res["r"]))
            x_str = _truncate_number(str(res["x"]))
            y_str = _truncate_number(str(res["y"])) if res["y"] is not None else "—"
            passed = "✓" if res["verification_passed"] else "✗"

            table.add_row([
                res["iteration"],
                r_str,
                x_str,
                res["bits"],
                y_str,
                passed,
            ])

        click.echo(table)

    except Exception as e:
        click.echo(f"Ошибка при выполнении протокола: {e}")


def _truncate_number(s: str, max_len: int = 20) -> str:
    """Обрезает длинные числа для красивого отображения в таблице."""
    if len(s) <= max_len:
        return s
    return s[:8] + "..." + s[-8:]
