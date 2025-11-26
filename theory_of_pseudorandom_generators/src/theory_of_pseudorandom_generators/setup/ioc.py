from collections.abc import Iterable
from typing import Final

from dishka import Provider, Scope

from theory_of_pseudorandom_generators.application.commands.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback import (
    FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler,
)
from theory_of_pseudorandom_generators.application.commands.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback import (
    GeffeyPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler,
)
from theory_of_pseudorandom_generators.application.commands.linear_congruent_pseudorandom_number_generator import (
    LinearCongruentPseudorandomNumberGeneratorCommandHandler,
)
from theory_of_pseudorandom_generators.application.commands.methodology_for_assessing_the_quality_of_gpsp_distribution_on_plane import (
    MethodologyForAssessingTheQualityOfGpspDistributionOnPlaneCommandHandler,
)
from theory_of_pseudorandom_generators.application.commands.methodology_for_assessing_the_quality_of_gpsp_evaluation_tests_checking_unlinked_series import (
    MethodologyForAssessingTheQualityOfGpspEvaluationTestsCheckingUnlinkedSeriesCommandHandler,
)
from theory_of_pseudorandom_generators.application.commands.methodology_for_assessing_the_quality_of_gpsp_histogram_of_the_distribution_of_elements import (
    MethodologyForAssessingTheQualityOfGpspHistogramOfTheDistributionOfElementsCommandHandler,
)
from theory_of_pseudorandom_generators.application.commands.polynomial_congruent_pseudorandom_number_generator import (
    PolynomialCongruentPseudorandomNumberGeneratorCommandHandler,
)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.ports.register_id_generator import (
    RegisterIDGenerator,
)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.services.register_service import (
    RegisterService,
)
from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.ports.geffe_generator_id_generator import (
    GeffeGeneratorIDGenerator,
)
from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.services.geffe_generator_service import (
    GeffeGeneratorService,
)
from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.ports.linear_congruent_id_generator import (
    LinearCongruentIDGenerator,
)
from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.services.linear_congruent_generator_service import (
    LinearCongruentGeneratorService,
)
from theory_of_pseudorandom_generators.domain.methodology_for_assessing_the_quality_of_gpsp_distribution_on_plane.services.plane_distribution_service import (
    PlaneDistributionService,
)
from theory_of_pseudorandom_generators.domain.methodology_for_assessing_the_quality_of_gpsp_evaluation_tests_checking_unlinked_series.services.nist_test_service import (
    NISTTestService,
)
from theory_of_pseudorandom_generators.domain.methodology_for_assessing_the_quality_of_gpsp_histogram_of_the_distribution_of_elements.services.histogram_service import (
    HistogramService,
)
from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.ports.polynomial_congruent_id_generator import (
    PolynomialCongruentIDGenerator,
)
from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.services.polynomial_congruent_generator_service import (
    PolynomialCongruentGeneratorService,
)
from theory_of_pseudorandom_generators.infrastructure.id_generators import (
    UUID4GeffeGeneratorIDGenerator,
    UUID4LinearCongruentIDGenerator,
    UUID4PolynomialCongruentIDGenerator,
    UUID4RegisterIDGenerator,
)


def interactors_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide_all(
        FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler,
        GeffeyPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler,
        LinearCongruentPseudorandomNumberGeneratorCommandHandler,
        MethodologyForAssessingTheQualityOfGpspDistributionOnPlaneCommandHandler,
        MethodologyForAssessingTheQualityOfGpspEvaluationTestsCheckingUnlinkedSeriesCommandHandler,
        MethodologyForAssessingTheQualityOfGpspHistogramOfTheDistributionOfElementsCommandHandler,
        PolynomialCongruentPseudorandomNumberGeneratorCommandHandler
    )

    return provider


def id_generators_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide(source=UUID4RegisterIDGenerator, provides=RegisterIDGenerator)
    provider.provide(source=UUID4GeffeGeneratorIDGenerator, provides=GeffeGeneratorIDGenerator)
    provider.provide(source=UUID4PolynomialCongruentIDGenerator, provides=PolynomialCongruentIDGenerator)
    provider.provide(source=UUID4LinearCongruentIDGenerator, provides=LinearCongruentIDGenerator)
    return provider


def services_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide_all(
        RegisterService,
        GeffeGeneratorService,
        LinearCongruentGeneratorService,
        PlaneDistributionService,
        NISTTestService,
        HistogramService,
        PolynomialCongruentGeneratorService
    )
    return provider


def setup_providers() -> Iterable[Provider]:
    return (
        interactors_provider(),
        id_generators_provider(),
        services_provider(),
    )
