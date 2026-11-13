from dishka import Provider, Scope, from_context, provide

from blast_furnace.application.calculate_temperature import (
    CalculateTemperature,
    CalculationLog,
)
from blast_furnace.application.get_blast_reference import GetBlastReference
from blast_furnace.infrastructure.calculation_log import FileCalculationLog
from blast_furnace.setup.config import Settings


class ApplicationProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)
    reference_query = provide(GetBlastReference, scope=Scope.REQUEST)
    calculate_temperature = provide(CalculateTemperature, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def calculation_log(self, settings: Settings) -> CalculationLog:
        return FileCalculationLog(settings.log_path)
