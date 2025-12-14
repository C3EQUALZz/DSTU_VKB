"""Команда для выполнения протокола идентификации с нулевой передачей данных."""
import logging
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.zero_knowledge_proof import (
    ZeroKnowledgeProofExecutionView
)
from cryptography_methods.domain.zero_knowledge_proof.services.zero_knowledge_proof_service import (
    ProtocolKeys,
    ZeroKnowledgeProofService,
    ProtocolResult
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ExecuteZeroKnowledgeProofCommand:
    iterations: int
    bit_length: int
    random_values: list[int] | None = None
    keys: ProtocolKeys | None = None  # Если ключи уже сгенерированы


@final
class ExecuteZeroKnowledgeProofCommandHandler:
    def __init__(self, zero_knowledge_proof_service: ZeroKnowledgeProofService) -> None:
        self._zero_knowledge_proof_service: Final[ZeroKnowledgeProofService] = (
            zero_knowledge_proof_service
        )

    async def __call__(
        self, data: ExecuteZeroKnowledgeProofCommand
    ) -> ZeroKnowledgeProofExecutionView:
        logger.info(
            f"Executing zero-knowledge proof protocol: {data.iterations} iterations, "
            f"{data.bit_length}-bit primes"
        )

        # Генерируем ключи, если они не предоставлены
        if data.keys is None:
            keys: ProtocolKeys = self._zero_knowledge_proof_service.generate_keys(data.bit_length)
        else:
            keys = data.keys

        # Выполняем протокол
        result: ProtocolResult = self._zero_knowledge_proof_service.execute_protocol(
            keys=keys,
            iterations=data.iterations,
            random_values=data.random_values
        )

        logger.info("Protocol execution completed successfully")

        return ZeroKnowledgeProofExecutionView(
            p=str(keys.p),
            q=str(keys.q),
            n=str(keys.n),
            v=str(keys.v),
            s=str(keys.s),
            total_iterations=result.total_iterations,
            failed_attempts=result.failed_attempts,
            failure_rate=result.failure_rate,
            authentication_passed=result.authentication_passed,
            iterations=[
                {
                    "iteration": iter_result.iteration_number,
                    "r": str(iter_result.r),
                    "x": str(iter_result.x),
                    "b": iter_result.b,
                    "y": str(iter_result.y) if iter_result.y is not None else None,
                    "verification_passed": iter_result.verification_passed,
                }
                for iter_result in result.iterations
            ],
        )

