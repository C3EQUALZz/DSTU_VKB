from typing import Final, Iterable

from dishka import Provider, Scope

from mathematical_algorithms_of_geometry_in_cryptography.application.commands.find_divisor import (
    FindDivisorCommandHandler
)
from mathematical_algorithms_of_geometry_in_cryptography.application.commands.elliptic_curve_gfp_operations import (
    AddPointsCommandHandler,
    DoublePointCommandHandler,
    FindAllOrdersCommandHandler,
    FindPointOrderCommandHandler,
    GenerateEllipticCurveGFpCommandHandler,
    GenerateSequenceCommandHandler,
    MultiplyPointCommandHandler,
)
from mathematical_algorithms_of_geometry_in_cryptography.application.commands.generate_elliptic_curve import (
    GenerateEllipticCurveCommandHandler
)
from mathematical_algorithms_of_geometry_in_cryptography.application.commands.miller_rabit_test import (
    MakeMillerRabitTestCommandHandler
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve import EllipticCurveService
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.ports.elliptic_curve_id_generator import (
    EllipticCurveIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp import EllipticCurveGFpService
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.ports.elliptic_curve_gfp_id_generator import (
    EllipticCurveGFpIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin import MillerRabinService
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.ports.miller_rabin_id_generator import (
    MillerRabinIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho import PollardRhoService
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.ports.pollard_rho_id_generator import (
    PollardRhoIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.infrastructure.adapters.uuid4_elliptic_curve_gfp_id_generator import (
    UUID4EllipticCurveGFpIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.infrastructure.adapters.uuid4_elleptic_curve_id_generator import (
    UUID4EllipticCurveIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.infrastructure.adapters.uuid4_miller_rabin_id_generator import (
    UUID4MillerRabinIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.infrastructure.adapters.uuid4_pollard_rho_id_generator import (
    UUID4PollardRhoIDGenerator
)


def id_generators_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide(source=UUID4MillerRabinIDGenerator, provides=MillerRabinIDGenerator)
    provider.provide(source=UUID4PollardRhoIDGenerator, provides=PollardRhoIDGenerator)
    provider.provide(source=UUID4EllipticCurveIDGenerator, provides=EllipticCurveIDGenerator)
    provider.provide(source=UUID4EllipticCurveGFpIDGenerator, provides=EllipticCurveGFpIDGenerator)
    return provider


def services_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide_all(
        MillerRabinService,
        PollardRhoService,
        EllipticCurveService,
        EllipticCurveGFpService,
    )
    return provider


def interactors_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)

    provider.provide_all(
        MakeMillerRabitTestCommandHandler,
        FindDivisorCommandHandler,
        GenerateEllipticCurveCommandHandler,
        GenerateEllipticCurveGFpCommandHandler,
        AddPointsCommandHandler,
        DoublePointCommandHandler,
        MultiplyPointCommandHandler,
        FindPointOrderCommandHandler,
        FindAllOrdersCommandHandler,
        GenerateSequenceCommandHandler,
    )

    return provider


def setup_providers() -> Iterable[Provider]:
    return (
        id_generators_provider(),
        services_provider(),
        interactors_provider(),
    )
