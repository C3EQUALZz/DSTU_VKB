from app.infrastructure.services.block_codes import BlockCodesService
from app.infrastructure.services.convolutional_codes import \
    ConvolutionalCodesService
from app.infrastructure.services.cyclic_codes import CyclicCodeService
from app.infrastructure.services.field_calculator import FieldCalculatorService
from app.infrastructure.services.interleaver import InterleaveService
from app.logic.use_cases.calculator import EvaluateMathExpressionInFieldUseCase
from app.logic.use_cases.cascade_codes import (DecodeCascadeCodeUseCase,
                                               EncodeCascadeCodeUseCase,
                                               ShowNoisyImageUseCase)
from app.logic.use_cases.convolutional_codes import (
    DecodeConvolutionalCodeUseCase, EncodeConvolutionalCodeUseCase)
from app.logic.use_cases.cyclic_codes import EncodeCyclicCodeMatrixUseCase, EncodeCyclicCodePolynomUseCase, \
    DecodeCyclicCodePolynomUseCase
from app.settings.config import Settings
from dishka import Provider, Scope, from_context, make_async_container, provide
from redis.asyncio import ConnectionPool, Redis


class RedisProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_connection_pool(self, settings: Settings) -> ConnectionPool:
        return ConnectionPool.from_url(
            str(settings.cache.url), encoding="utf8", decode_responses=True
        )

    @provide(scope=Scope.APP)
    async def get_client(self, pool: ConnectionPool) -> Redis:
        return Redis.from_pool(pool)


class FieldCalculatorUseCasesProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_evaluate_expression_use_case(
            self,
    ) -> EvaluateMathExpressionInFieldUseCase:
        return EvaluateMathExpressionInFieldUseCase(FieldCalculatorService())


class ConvolutionalCodeUseCasesProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_encode_expression_use_case(self) -> EncodeConvolutionalCodeUseCase:
        return EncodeConvolutionalCodeUseCase(ConvolutionalCodesService())

    @provide(scope=Scope.APP)
    async def get_decode_expression_use_case(self) -> DecodeConvolutionalCodeUseCase:
        return DecodeConvolutionalCodeUseCase(ConvolutionalCodesService())


class CascadeCodeUseCasesProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_encode_expression_use_case(self) -> EncodeCascadeCodeUseCase:
        return EncodeCascadeCodeUseCase(
            block_code=BlockCodesService(),
            interleave_service=InterleaveService(),
            convolutional_service=ConvolutionalCodesService(),
        )

    @provide(scope=Scope.APP)
    async def get_decode_expression_use_case(self) -> DecodeCascadeCodeUseCase:
        return DecodeCascadeCodeUseCase(
            block_code=BlockCodesService(),
            interleave_service=InterleaveService(),
            convolutional_service=ConvolutionalCodesService(),
        )

    @provide(scope=Scope.APP)
    async def get_noisy_image_use_case(self) -> ShowNoisyImageUseCase:
        return ShowNoisyImageUseCase()


class CyclicCodeUseCasesProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_encode_expression_matrix_use_case(self) -> EncodeCyclicCodeMatrixUseCase:
        return EncodeCyclicCodeMatrixUseCase(CyclicCodeService())

    @provide(scope=Scope.APP)
    async def get_encode_expression_polynomials_use_case(self) -> EncodeCyclicCodePolynomUseCase:
        return EncodeCyclicCodePolynomUseCase(CyclicCodeService())

    @provide(scope=Scope.APP)
    async def get_decode_expression_polynomials_use_case(self) -> DecodeCyclicCodePolynomUseCase:
        return DecodeCyclicCodePolynomUseCase(CyclicCodeService())


container = make_async_container(
    RedisProvider(),
    FieldCalculatorUseCasesProvider(),
    ConvolutionalCodeUseCasesProvider(),
    CascadeCodeUseCasesProvider(),
    CyclicCodeUseCasesProvider(),
    context={
        Settings: Settings(),
    },
)
