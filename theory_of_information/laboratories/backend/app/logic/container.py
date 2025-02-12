from dishka import (
    from_context,
    make_async_container,
    provide,
    Provider,
    Scope,
)
from redis.asyncio import ConnectionPool, Redis

from app.infrastructure.services.field_calculator import FieldCalculatorService
from app.logic.use_cases.calculator import EvaluateMathExpressionInFieldUseCase
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


container = make_async_container(
    RedisProvider(),
    FieldCalculatorUseCasesProvider(),
    context={
        Settings: Settings(),
    }
)
