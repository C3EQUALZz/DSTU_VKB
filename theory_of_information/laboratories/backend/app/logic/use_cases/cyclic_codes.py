import random
import re

from app.exceptions.logic import StringMustContainsOnlyNumberException
from app.infrastructure.services.cyclic_codes import CyclicCodeService
from app.logic.commands.cyclic_codes import EncodeCyclicCodeWithMatrixCommand, EncodeCyclicCodeWithPolynomCommand, \
    DecodeCyclicCodeWithPolynomCommand
from app.logic.dtos.cyclic_codes import EncodedAndPolynomDTO, EncodedAndMatrixDTO
from app.logic.use_cases.base import BaseUseCase


class EncodeCyclicCodeMatrixUseCase(BaseUseCase[EncodeCyclicCodeWithMatrixCommand]):
    def __init__(self, service: CyclicCodeService) -> None:
        self._service: CyclicCodeService = service

    async def __call__(self, command: EncodeCyclicCodeWithMatrixCommand) -> EncodedAndPolynomDTO:
        symbols_to_encode: str = command.data

        if re.match(r"[a-zA-Zа-яА-Я]+", command.data):
            raise StringMustContainsOnlyNumberException()

        return self._service.encode(symbols_to_encode, command.matrix)


class EncodeCyclicCodePolynomUseCase(BaseUseCase[EncodeCyclicCodeWithPolynomCommand]):
    def __init__(self, service: CyclicCodeService) -> None:
        self._service: CyclicCodeService = service

    async def __call__(self, command: EncodeCyclicCodeWithPolynomCommand) -> EncodedAndMatrixDTO:
        polynomials: list[str] = re.findall(r'\((.*?)\)', command.polynom)

        coeffs: list[int] = self._service.pols_to_coefficients(random.choice(polynomials))

        matrix: list[list[int]] = [
            coeffs + [0] * (command.n - len(coeffs))
        ]

        m: int = len(matrix[0]) - len(matrix)

        for shift in range(m):
            row: list[int] = matrix[-1]
            matrix.append(self._service.cyclic_shift(row, 1))

        result: EncodedAndPolynomDTO = self._service.encode(
            symbols_to_encode=command.data,
            matrix=matrix,
        )

        return EncodedAndMatrixDTO(
            encoded=result.encoded,
            matrix=matrix,
        )


class DecodeCyclicCodePolynomUseCase(BaseUseCase[DecodeCyclicCodeWithPolynomCommand]):
    def __init__(self, service: CyclicCodeService) -> None:
        self._service: CyclicCodeService = service

    async def __call__(self, command: DecodeCyclicCodeWithPolynomCommand) -> str:
        return self._service.decode(v=command.data, g_poly_str=command.polynom)
