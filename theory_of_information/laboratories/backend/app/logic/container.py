from dishka import (
    from_context,
    make_async_container,
    provide,
    Provider,
    Scope,
)
from redis.asyncio import ConnectionPool, Redis

from app.infrastructure.services.field_calculator import FieldCalculatorService
from app.infrastructure.services.convolutional_codes import ConvolutionalCodesService
from app.logic.use_cases.calculator import EvaluateMathExpressionInFieldUseCase
from app.logic.use_cases.convolutional_codes import EncodeConvolutionalCodeUseCase, DecodeConvolutionalCodeUseCase
from app.settings.config import Settings


class RedisProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_connection_pool(self, settings: Settings) -> ConnectionPool:
        return ConnectionPool.from_url(str(settings.cache.url), encoding="utf8", decode_responses=True)

    @provide(scope=Scope.APP)
    async def get_client(self, pool: ConnectionPool) -> Redis:
        return Redis.from_pool(pool)


class FieldCalculatorUseCasesProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_evaluate_expression_use_case(self) -> EvaluateMathExpressionInFieldUseCase:
        return EvaluateMathExpressionInFieldUseCase(FieldCalculatorService())


class ConvolutionalCodeUseCasesProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_encode_expression_use_case(self) -> EncodeConvolutionalCodeUseCase:
        return EncodeConvolutionalCodeUseCase(ConvolutionalCodesService())

    @provide(scope=Scope.APP)
    async def get_decode_expression_use_case(self) -> DecodeConvolutionalCodeUseCase:
        return DecodeConvolutionalCodeUseCase(ConvolutionalCodesService())


container = make_async_container(
    RedisProvider(),
    FieldCalculatorUseCasesProvider(),
    ConvolutionalCodeUseCasesProvider(),
    context={
        Settings: Settings(),
    }
)
