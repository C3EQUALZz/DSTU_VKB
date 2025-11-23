from uuid import uuid4

from typing_extensions import override

from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.ports.register_id_generator import (
    RegisterIDGenerator,
)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.values.register_id import (
    RegisterID,
)
from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.ports.linear_congruent_id_generator import (
    LinearCongruentIDGenerator,
)
from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.values.linear_congruent_generator_id import (
    LinearCongruentGeneratorID,
)
from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.ports.polynomial_congruent_id_generator import (
    PolynomialCongruentIDGenerator,
)
from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.values.polynomial_congruent_generator_id import (
    PolynomialCongruentGeneratorID,
)
from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.ports.geffe_generator_id_generator import (
    GeffeGeneratorIDGenerator,
)
from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.values.geffe_generator_id import (
    GeffeGeneratorID,
)


class UUID4LinearCongruentIDGenerator(LinearCongruentIDGenerator):
    @override
    def __call__(self) -> LinearCongruentGeneratorID:
        return LinearCongruentGeneratorID(uuid4())


class UUID4PolynomialCongruentIDGenerator(PolynomialCongruentIDGenerator):
    @override
    def __call__(self) -> PolynomialCongruentGeneratorID:
        return PolynomialCongruentGeneratorID(uuid4())


class UUID4RegisterIDGenerator(RegisterIDGenerator):
    @override
    def __call__(self) -> RegisterID:
        return RegisterID(uuid4())


class UUID4GeffeGeneratorIDGenerator(GeffeGeneratorIDGenerator):
    @override
    def __call__(self) -> GeffeGeneratorID:
        return GeffeGeneratorID(uuid4())
