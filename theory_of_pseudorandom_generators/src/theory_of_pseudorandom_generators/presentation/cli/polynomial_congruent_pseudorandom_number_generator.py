import click
from dishka import FromDishka

from theory_of_pseudorandom_generators.application.commands.polynomial_congruent_pseudorandom_number_generator import (
    PolynomialCongruentPseudorandomNumberGeneratorCommand,
    PolynomialCongruentPseudorandomNumberGeneratorCommandHandler,
)


@click.group(name="polynomial_congruent_pseudorandom_number_generator")
def polynomial_congruent_pseudorandom_number_generator_group() -> None:
    ...


@polynomial_congruent_pseudorandom_number_generator_group.command(name="generate")
@click.option("-a1", required=True, help="a number for generate sequence", type=int)
@click.option("-a2", required=True, help="a number for generate sequence", type=int)
@click.option("-b", required=True, help="b number for generate sequence", type=int)
@click.option("-m", required=True, help="m number for generate sequence", type=int)
@click.option("-x0", required=True, help="x0 start number for generate sequence", type=int)
@click.option("-s", "--size", required=True, help="size of sequence", type=int, default=200)
def cmd_generate_handler(
        a1: int,
        a2: int,
        b: int,
        m: int,
        x0: int,
        size: int,
        interactor: FromDishka[PolynomialCongruentPseudorandomNumberGeneratorCommandHandler]
) -> None:
    command: PolynomialCongruentPseudorandomNumberGeneratorCommand = PolynomialCongruentPseudorandomNumberGeneratorCommand(
        a1=a1,
        a2=a2,
        b=b,
        m=m,
        x0=x0,
        size=size,
    )

    interactor(command)
