"""CLI handlers для протокола идентификации с нулевой передачей данных."""
import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.zero_knowledge_proof.execute import (
    ExecuteZeroKnowledgeProofCommand,
    ExecuteZeroKnowledgeProofCommandHandler
)
from cryptography_methods.application.common.views.zero_knowledge_proof import (
    ZeroKnowledgeProofExecutionView
)
from cryptography_methods.domain.zero_knowledge_proof.services.modular_arithmetic_service import (
    ModularArithmeticService
)
from cryptography_methods.domain.zero_knowledge_proof.services.prime_number_service import (
    PrimeNumberService
)
from cryptography_methods.domain.zero_knowledge_proof.services.quadratic_residue_service import (
    QuadraticResidueService
)
from cryptography_methods.domain.zero_knowledge_proof.services.zero_knowledge_proof_service import (
    ZeroKnowledgeProofService
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
    default=256,
    help="Bit length for prime numbers (default: 256)",
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
        click.echo("Error: iterations must be a positive integer")
        return

    if bit_length < 64:
        click.echo("Error: bit_length must be at least 64")
        return

    # Создаем сервисы для генерации ключей (используем DI контейнер через interactor)
    # Но нам нужно сначала получить сервис для генерации ключей
    # Для этого создадим временный сервис или используем существующий через DI
    
    # Временно создаем сервисы напрямую для генерации ключей
    # В идеале это должно быть через DI, но для CLI это приемлемо
    modular_service = ModularArithmeticService()
    prime_service = PrimeNumberService(modular_service)
    quadratic_service = QuadraticResidueService(modular_service)
    zkp_service = ZeroKnowledgeProofService(prime_service, quadratic_service, modular_service)

    click.echo("Генерация ключей протокола...")
    keys = zkp_service.generate_keys(bit_length)

    click.echo(f"\nСгенерированные простые числа:")
    click.echo(f"p = {keys.p}")
    click.echo(f"q = {keys.q}")
    click.echo(f"n = p * q = {keys.n}")
    
    click.echo(f"\nПоиск случайного квадратичного вычета V по модулю n...")
    click.echo(f"Найден квадратичный вычет V: {keys.v} (Открытый ключ)")
    
    click.echo(f"\nЗакрытый ключ S: {keys.s}")

    # Если тестируем неудачную аутентификацию, используем неправильный ключ
    wrong_key: int | None = None
    if test_failure:
        # Генерируем случайный неправильный ключ
        import secrets
        wrong_key = secrets.randbelow(keys.n)
        click.echo(f"\n⚠️  ТЕСТОВЫЙ РЕЖИМ: Используется неправильный секретный ключ = {wrong_key}")
        click.echo("   (Аутентификация должна не пройти при b=1)")

    # Выполняем протокол пошагово - для каждой итерации запрашиваем r и сразу выполняем
    click.echo("\n" + "=" * 60)
    click.echo("Выполнение протокола...")
    click.echo("=" * 60)
    click.echo("\nОбъяснение логики протокола:")
    click.echo("1. При b=0: проверка x = r² mod n всегда проходит (x вычисляется именно так)")
    click.echo("2. При b=1: проверка x = y² * V mod n проходит ТОЛЬКО если используется правильный секретный ключ S")
    click.echo("3. Если кто-то не знает S, то при b=1 проверка не пройдет")
    click.echo("4. Протокол повторяется несколько раз, чтобы снизить вероятность угадывания")
    click.echo("=" * 60)

    protocol_results: list[dict] = []
    failed_attempts = 0
    used_r: set[int] = set()

    for i in range(iterations):
        click.echo(f"\nИтерация {i + 1}:")
        
        # Запрашиваем r
        while True:
            try:
                r_input = click.prompt(
                    f"Введите случайное число r (0 < r < {keys.n})",
                    type=str
                )
                r = int(r_input)

                if r <= 0 or r >= keys.n:
                    click.echo(f"Ошибка: r должно быть в диапазоне (0, {keys.n})")
                    continue

                if r in used_r:
                    click.echo("Ошибка: это число уже использовалось")
                    continue

                used_r.add(r)
                break
            except ValueError:
                click.echo("Ошибка: введено не число")
            except click.Abort:
                click.echo("\nОперация отменена")
                return

        # Выполняем одну итерацию протокола
        iteration_result = zkp_service.execute_single_iteration(keys, r, i + 1, wrong_key)

        # Выводим результаты итерации сразу
        x = iteration_result.x
        b = iteration_result.b
        click.echo(f"A → B: x = r² mod n = {x}")
        click.echo(f"B → A: b = {b}")
        click.echo(f"Выбран бит b = {b}")

        if b == 0:
            click.echo(f"A → B: r = {r}")
            if iteration_result.verification_passed:
                click.echo("B: Проверка пройдена (x = r² mod n)")
                click.echo("   (Примечание: при b=0 проверка всегда проходит, так как x = r² mod n по определению)")
            else:
                click.echo("B: Ошибка проверки!")
                failed_attempts += 1
        else:
            y = iteration_result.y
            if y is not None:
                click.echo(f"A → B: y = r * S mod n = {y}")
            if iteration_result.verification_passed:
                click.echo("B: Проверка пройдена (y² * V mod n = x)")
                click.echo("   (Примечание: при b=1 проверка проходит только если используется правильный секретный ключ S)")
            else:
                click.echo("B: Ошибка проверки!")
                click.echo("   (Примечание: проверка не прошла, потому что использован неправильный секретный ключ)")
                failed_attempts += 1

        # Сохраняем результат
        protocol_results.append({
            "iteration": iteration_result.iteration_number,
            "r": str(iteration_result.r),
            "x": str(iteration_result.x),
            "b": iteration_result.b,
            "y": str(iteration_result.y) if iteration_result.y is not None else None,
            "verification_passed": iteration_result.verification_passed,
        })

    # Выводим итоговые результаты
    failure_rate = failed_attempts / iterations
    authentication_passed = failure_rate <= 0.01

    click.echo("\n" + "=" * 60)
    click.echo("Результаты:")
    click.echo(f"- Всего итераций: {iterations}")
    click.echo(f"- Неудачных попыток: {failed_attempts}")
    click.echo(f"- Процент неудач: {failure_rate:.1%}")

    if authentication_passed:
        click.echo("\nАутентификация пройдена успешно!")
    else:
        click.echo("\nАутентификация НЕ пройдена. Процент неудач превышает 1%.")

    # Создаем view для совместимости (хотя уже все вывели)
    try:
        view = ZeroKnowledgeProofExecutionView(
            p=str(keys.p),
            q=str(keys.q),
            n=str(keys.n),
            v=str(keys.v),
            s=str(keys.s),
            total_iterations=iterations,
            failed_attempts=failed_attempts,
            failure_rate=failure_rate,
            authentication_passed=authentication_passed,
            iterations=protocol_results
        )


    except Exception as e:
        click.echo(f"Error during protocol execution: {e}")

