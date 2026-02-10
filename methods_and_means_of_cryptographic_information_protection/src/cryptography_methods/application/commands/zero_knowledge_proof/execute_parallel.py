"""Команда для выполнения параллельной схемы протокола идентификации с нулевой передачей данных."""
import logging
import secrets
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.zero_knowledge_proof import (
    ParallelZeroKnowledgeProofExecutionView
)
from cryptography_methods.domain.zero_knowledge_proof.services.modular_arithmetic_service import (
    ModularArithmeticService
)
from cryptography_methods.domain.zero_knowledge_proof.services.parallel_zero_knowledge_proof_service import (
    ParallelProtocolKeys,
    ParallelZeroKnowledgeProofService,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ExecuteParallelZeroKnowledgeProofCommand:
    iterations: int    # t — количество итераций (циклов)
    bit_length: int    # длина простых чисел в битах
    k: int             # K — количество пар ключей
    test_failure: bool = False


@final
class ExecuteParallelZeroKnowledgeProofCommandHandler:
    def __init__(
        self,
        parallel_zkp_service: ParallelZeroKnowledgeProofService,
        modular_arithmetic_service: ModularArithmeticService,
    ) -> None:
        self._parallel_zkp_service: Final[ParallelZeroKnowledgeProofService] = parallel_zkp_service
        self._modular_arithmetic: Final[ModularArithmeticService] = modular_arithmetic_service

    async def __call__(
        self, data: ExecuteParallelZeroKnowledgeProofCommand
    ) -> ParallelZeroKnowledgeProofExecutionView:
        k = data.k
        t = data.iterations

        logger.info(
            "============================================================\n"
            "ПАРАЛЛЕЛЬНАЯ СХЕМА ПРОТОКОЛА ИДЕНТИФИКАЦИИ\n"
            "С НУЛЕВОЙ ПЕРЕДАЧЕЙ ДАННЫХ\n"
            "(Схема Фейге-Фиата-Шамира, параллельная версия)\n"
            f"K = {k}, t = {t}\n"
            "============================================================"
        )

        # === 1. Генерация ключей ===
        logger.info("Генерация ключей протокола...")
        keys: ParallelProtocolKeys = self._parallel_zkp_service.generate_keys(
            bit_length=data.bit_length,
            k=k,
        )

        logger.info(
            f"\nЗначение n:\n"
            f"  p = {keys.p}\n"
            f"  q = {keys.q}\n"
            f"  n = p * q = {keys.n}"
        )

        # Выводим открытые и секретные ключи
        logger.info("\nОткрытые ключи (квадратичные вычеты по модулю n):")
        for i in range(k):
            v = keys.public_keys[i]
            v_inv = self._modular_arithmetic.mod_inverse(v, keys.n)
            if v_inv is None:
                raise ValueError(f"Cannot compute V{i + 1}⁻¹ mod n")
            logger.info(
                f"  V{i + 1} = {v}\n"
                f"    V{i + 1}⁻¹ mod n = {v_inv}\n"
                f"    Проверка: V{i + 1} * V{i + 1}⁻¹ mod n = {(v * v_inv) % keys.n} (должно быть 1)"
            )

        logger.info("\nСекретные ключи (Si = √(Vi⁻¹) mod n, наименьшее значение):")
        for i in range(k):
            s = keys.secret_keys[i]
            v = keys.public_keys[i]
            v_inv = self._modular_arithmetic.mod_inverse(v, keys.n)
            if v_inv is None:
                raise ValueError(f"Cannot compute V{i + 1}⁻¹ mod n")
            logger.info(
                f"  S{i + 1} = {s}\n"
                f"    Проверка: S{i + 1}² mod n = {pow(s, 2, keys.n)} "
                f"(должно быть {v_inv}, т.е. V{i + 1}⁻¹ mod n)"
            )

        # === 2. Определяем секретные ключи для протокола ===
        wrong_keys: list[int] | None = None
        if data.test_failure:
            wrong_keys = [secrets.randbelow(keys.n - 2) + 1 for _ in range(k)]
            logger.info(
                f"\n⚠️  ТЕСТОВЫЙ РЕЖИМ: Используются НЕПРАВИЛЬНЫЕ секретные ключи\n"
                + "\n".join(f"   S{i + 1}' = {wk}" for i, wk in enumerate(wrong_keys))
                + "\n   (Аутентификация должна провалиться)"
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

        for i in range(t):
            r = self._generate_unique_r(keys.n, used_r)
            used_r.add(r)

            iter_result = self._parallel_zkp_service.execute_single_iteration(
                keys=keys,
                r=r,
                iteration_number=i + 1,
                wrong_secret_keys=wrong_keys,
            )

            bits = iter_result.bits
            bits_str = "".join(str(b) for b in bits)
            x = iter_result.x
            y = iter_result.y
            secret_keys_used = wrong_keys if wrong_keys is not None else keys.secret_keys

            # Логируем шаги протокола
            logger.info(f"\n--- Итерация {i + 1}/{t} ---")

            logger.info(
                f"  Сторона А:\n"
                f"    Выбирает r = {r}\n"
                f"    Вычисляет x = r² mod n = {r}² mod {keys.n} = {x}\n"
                f"    Отправляет x = {x} стороне В"
            )

            logger.info(
                f"  Сторона В:\n"
                f"    Генерирует случайную двоичную строку из K={k} бит:\n"
                f"    [{bits_str}] = ({', '.join(f'b{j + 1}={bits[j]}' for j in range(k))})\n"
                f"    Отправляет строку стороне А"
            )

            # Формируем описание вычисления y
            s_factors = []
            for j in range(k):
                if bits[j] == 1:
                    s_factors.append(f"S{j + 1}")
            if s_factors:
                s_product_desc = " × ".join(s_factors)
                s_product_vals = " × ".join(
                    str(secret_keys_used[j]) for j in range(k) if bits[j] == 1
                )
                logger.info(
                    f"  Сторона А:\n"
                    f"    Вычисляет y = r × ({s_product_desc}) mod n\n"
                    f"    y = {r} × ({s_product_vals}) mod {keys.n} = {y}\n"
                    f"    Отправляет y = {y} стороне В"
                )
            else:
                logger.info(
                    f"  Сторона А:\n"
                    f"    Все bi=0, поэтому y = r = {r}\n"
                    f"    Отправляет y = {y} стороне В"
                )

            # Формируем описание проверки стороны В
            v_factors = []
            for j in range(k):
                if bits[j] == 1:
                    v_factors.append(f"V{j + 1}")
            if v_factors:
                v_product_desc = " × ".join(v_factors)
                v_product_vals = " × ".join(
                    str(keys.public_keys[j]) for j in range(k) if bits[j] == 1
                )
                check_val = pow(y, 2, keys.n)
                for j in range(k):
                    if bits[j] == 1:
                        check_val = (check_val * keys.public_keys[j]) % keys.n
            else:
                v_product_desc = "(нет множителей, все bi=0)"
                v_product_vals = ""
                check_val = pow(y, 2, keys.n)

            if iter_result.verification_passed:
                if v_factors:
                    logger.info(
                        f"  Сторона В (проверка):\n"
                        f"    Проверяет: x = y² × ({v_product_desc}) mod n\n"
                        f"    y² × ({v_product_vals}) mod {keys.n} = {check_val}\n"
                        f"    Результат: {check_val} == {x} ✓ ПРОВЕРКА ПРОЙДЕНА"
                    )
                else:
                    logger.info(
                        f"  Сторона В (проверка):\n"
                        f"    Проверяет: x = y² mod n (все bi=0)\n"
                        f"    y² mod {keys.n} = {check_val}\n"
                        f"    Результат: {check_val} == {x} ✓ ПРОВЕРКА ПРОЙДЕНА"
                    )
            else:
                failed_attempts += 1
                if v_factors:
                    logger.info(
                        f"  Сторона В (проверка):\n"
                        f"    Проверяет: x = y² × ({v_product_desc}) mod n\n"
                        f"    y² × ({v_product_vals}) mod {keys.n} = {check_val}\n"
                        f"    Результат: {check_val} != {x} ✗ ПРОВЕРКА НЕ ПРОЙДЕНА"
                    )
                else:
                    logger.info(
                        f"  Сторона В (проверка):\n"
                        f"    Проверяет: x = y² mod n (все bi=0)\n"
                        f"    y² mod {keys.n} = {check_val}\n"
                        f"    Результат: {check_val} != {x} ✗ ПРОВЕРКА НЕ ПРОЙДЕНА"
                    )

            iteration_results.append({
                "iteration": iter_result.iteration_number,
                "r": str(iter_result.r),
                "x": str(iter_result.x),
                "bits": bits_str,
                "y": str(iter_result.y),
                "verification_passed": iter_result.verification_passed,
            })

        # === 4. Итоги ===
        failure_rate = failed_attempts / t if t > 0 else 0.0
        cheat_probability = (1 / 2) ** (k * t)
        authentication_passed = failed_attempts == 0

        logger.info(
            "\n============================================================\n"
            "ИТОГОВЫЕ РЕЗУЛЬТАТЫ\n"
            "============================================================"
        )
        logger.info(
            f"Параметры: K = {k}, t = {t}\n"
            f"Всего итераций: {t}\n"
            f"Неудачных проверок: {failed_attempts}\n"
            f"Вероятность обмана: (1/2)^(K×t) = (1/2)^({k}×{t}) = (1/2)^{k * t} = {cheat_probability:.10f}"
        )

        if authentication_passed:
            logger.info(
                "✓ АУТЕНТИФИКАЦИЯ ПРОЙДЕНА УСПЕШНО\n"
                f"  Сторона А доказала знание секретных ключей S1..S{k} без их раскрытия."
            )
        else:
            logger.info(
                "✗ АУТЕНТИФИКАЦИЯ НЕ ПРОЙДЕНА\n"
                f"  Сторона А не смогла доказать знание секретных ключей."
            )

        return ParallelZeroKnowledgeProofExecutionView(
            p=str(keys.p),
            q=str(keys.q),
            n=str(keys.n),
            k=k,
            public_keys=[str(v) for v in keys.public_keys],
            secret_keys=[str(s) for s in keys.secret_keys],
            total_iterations=t,
            failed_attempts=failed_attempts,
            failure_rate=failure_rate,
            cheat_probability=cheat_probability,
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

