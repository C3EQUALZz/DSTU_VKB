"""Команда для выполнения протокола идентификации с нулевой передачей данных."""
import logging
import secrets
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.zero_knowledge_proof import (
    ZeroKnowledgeProofExecutionView
)
from cryptography_methods.domain.zero_knowledge_proof.services.modular_arithmetic_service import (
    ModularArithmeticService
)
from cryptography_methods.domain.zero_knowledge_proof.services.zero_knowledge_proof_service import (
    ProtocolKeys,
    ZeroKnowledgeProofService,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ExecuteZeroKnowledgeProofCommand:
    iterations: int
    bit_length: int
    test_failure: bool = False


@final
class ExecuteZeroKnowledgeProofCommandHandler:
    def __init__(
        self,
        zero_knowledge_proof_service: ZeroKnowledgeProofService,
        modular_arithmetic_service: ModularArithmeticService,
    ) -> None:
        self._zkp_service: Final[ZeroKnowledgeProofService] = zero_knowledge_proof_service
        self._modular_arithmetic: Final[ModularArithmeticService] = modular_arithmetic_service

    async def __call__(
        self, data: ExecuteZeroKnowledgeProofCommand
    ) -> ZeroKnowledgeProofExecutionView:
        logger.info(
            "============================================================\n"
            "ПРОТОКОЛ ИДЕНТИФИКАЦИИ С НУЛЕВОЙ ПЕРЕДАЧЕЙ ДАННЫХ\n"
            "(Схема Фейге-Фиата-Шамира)\n"
            "============================================================"
        )

        # === 1. Генерация ключей ===
        logger.info("Генерация ключей протокола...")
        keys: ProtocolKeys = self._zkp_service.generate_keys(data.bit_length)

        # Вычисляем V^(-1) mod n для верификации
        v_inv: int | None = self._modular_arithmetic.mod_inverse(keys.v, keys.n)
        if v_inv is None:
            raise ValueError("Cannot compute V⁻¹ mod n")

        logger.info(
            f"\nЗначение n:\n"
            f"  p = {keys.p}\n"
            f"  q = {keys.q}\n"
            f"  n = p * q = {keys.n}"
        )
        logger.info(
            f"Открытый ключ V = {keys.v}\n"
            f"  (V — квадратичный вычет mod n, т.е. существует x: x² ≡ V (mod n))\n"
            f"  V⁻¹ mod n = {v_inv}\n"
            f"  Проверка: V * V⁻¹ mod n = {(keys.v * v_inv) % keys.n} (должно быть 1)"
        )
        logger.info(
            f"Секретный ключ S = {keys.s}\n"
            f"  (S = √(V⁻¹) mod n, наименьшее значение)\n"
            f"  Проверка: S² mod n = {pow(keys.s, 2, keys.n)} (должно быть {v_inv}, т.е. V⁻¹ mod n)"
        )

        # === 2. Определяем секретный ключ для протокола ===
        wrong_key: int | None = None
        if data.test_failure:
            wrong_key = secrets.randbelow(keys.n - 2) + 1
            logger.info(
                f"\n⚠️  ТЕСТОВЫЙ РЕЖИМ: Используется НЕПРАВИЛЬНЫЙ секретный ключ = {wrong_key}\n"
                f"   (Аутентификация должна провалиться при b=1)"
            )

        # === 3. Выполнение протокола ===
        logger.info(
            "\n============================================================\n"
            "ПРОЦЕСС ИДЕНТИФИКАЦИИ\n"
            "============================================================"
        )

        iteration_results: list[dict[str, int | str | bool | None]] = []
        failed_attempts = 0
        used_r: set[int] = set()

        for i in range(data.iterations):
            r = self._generate_unique_r(keys.n, used_r)
            used_r.add(r)

            iter_result = self._zkp_service.execute_single_iteration(
                keys=keys,
                r=r,
                iteration_number=i + 1,
                wrong_secret_key=wrong_key,
            )

            x = iter_result.x
            b = iter_result.b
            secret_used = wrong_key if wrong_key is not None else keys.s

            # Логируем шаги протокола
            logger.info(f"\n--- Итерация {i + 1}/{data.iterations} ---")

            logger.info(
                f"  Сторона А:\n"
                f"    Выбирает r = {r}\n"
                f"    Вычисляет x = r² mod n = {r}² mod {keys.n} = {x}\n"
                f"    Отправляет x = {x} стороне В"
            )
            logger.info(
                f"  Сторона В:\n"
                f"    Генерирует случайный бит b = {b}\n"
                f"    Отправляет b = {b} стороне А"
            )

            if b == 0:
                check_val = pow(r, 2, keys.n)
                logger.info(
                    f"  Сторона А (b=0):\n"
                    f"    Отправляет r = {r} стороне В"
                )
                if iter_result.verification_passed:
                    logger.info(
                        f"  Сторона В (проверка b=0):\n"
                        f"    Проверяет: x = r² mod n → {r}² mod {keys.n} = {check_val}\n"
                        f"    Результат: {check_val} == {x} ✓ ПРОВЕРКА ПРОЙДЕНА"
                    )
                else:
                    logger.info(
                        f"  Сторона В (проверка b=0):\n"
                        f"    Проверяет: x = r² mod n → {r}² mod {keys.n} = {check_val}\n"
                        f"    Результат: {check_val} != {x} ✗ ПРОВЕРКА НЕ ПРОЙДЕНА"
                    )
                    failed_attempts += 1
            else:
                y: int = iter_result.y if iter_result.y is not None else 0
                check_val = (y * y * keys.v) % keys.n
                logger.info(
                    f"  Сторона А (b=1):\n"
                    f"    Вычисляет y = r * S mod n = {r} * {secret_used} mod {keys.n} = {y}\n"
                    f"    Отправляет y = {y} стороне В"
                )
                if iter_result.verification_passed:
                    logger.info(
                        f"  Сторона В (проверка b=1):\n"
                        f"    Проверяет: x = y² * V mod n → {y}² * {keys.v} mod {keys.n} = {check_val}\n"
                        f"    Результат: {check_val} == {x} ✓ ПРОВЕРКА ПРОЙДЕНА"
                    )
                else:
                    logger.info(
                        f"  Сторона В (проверка b=1):\n"
                        f"    Проверяет: x = y² * V mod n → {y}² * {keys.v} mod {keys.n} = {check_val}\n"
                        f"    Результат: {check_val} != {x} ✗ ПРОВЕРКА НЕ ПРОЙДЕНА"
                    )
                    failed_attempts += 1

            iteration_results.append({
                "iteration": iter_result.iteration_number,
                "r": str(iter_result.r),
                "x": str(iter_result.x),
                "b": iter_result.b,
                "y": str(iter_result.y) if iter_result.y is not None else None,
                "verification_passed": iter_result.verification_passed,
            })

        # === 4. Итоги ===
        failure_rate = failed_attempts / data.iterations if data.iterations > 0 else 0.0
        authentication_passed = failed_attempts == 0

        logger.info(
            "\n============================================================\n"
            "ИТОГОВЫЕ РЕЗУЛЬТАТЫ\n"
            "============================================================"
        )
        logger.info(
            f"Всего итераций: {data.iterations}\n"
            f"Неудачных проверок: {failed_attempts}\n"
            f"Вероятность обмана: (1/2)^{data.iterations} = {(1 / 2) ** data.iterations:.10f}"
        )

        if authentication_passed:
            logger.info(
                "✓ АУТЕНТИФИКАЦИЯ ПРОЙДЕНА УСПЕШНО\n"
                "  Сторона А доказала знание секретного ключа S без его раскрытия."
            )
        else:
            logger.info(
                "✗ АУТЕНТИФИКАЦИЯ НЕ ПРОЙДЕНА\n"
                "  Сторона А не смогла доказать знание секретного ключа."
            )

        return ZeroKnowledgeProofExecutionView(
            p=str(keys.p),
            q=str(keys.q),
            n=str(keys.n),
            v=str(keys.v),
            s=str(keys.s),
            total_iterations=data.iterations,
            failed_attempts=failed_attempts,
            failure_rate=failure_rate,
            authentication_passed=authentication_passed,
            iterations=iteration_results,
        )

    def _generate_unique_r(self, n: int, used_r: set[int]) -> int:
        """Генерирует уникальное случайное r в диапазоне (0, n)."""
        max_attempts = 1000
        for _ in range(max_attempts):
            r = secrets.randbelow(n - 1) + 1
            if r not in used_r:
                return r
        raise RuntimeError(f"Не удалось сгенерировать уникальное r после {max_attempts} попыток")
