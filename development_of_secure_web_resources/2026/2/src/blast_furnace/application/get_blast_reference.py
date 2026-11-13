from blast_furnace.domain.reference import BLAST_PARAMETER_EFFECTS, BlastParameterEffect


class GetBlastReference:
    """Получить справочные данные для домашней страницы."""

    def execute(self) -> tuple[BlastParameterEffect, ...]:
        return BLAST_PARAMETER_EFFECTS
