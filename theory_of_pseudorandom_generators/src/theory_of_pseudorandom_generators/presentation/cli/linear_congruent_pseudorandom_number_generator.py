import click
from dishka import FromDishka

from theory_of_pseudorandom_generators.application.commands.linear_congruent_pseudorandom_number_generator import (
    LinearCongruentPseudorandomNumberGeneratorCommandHandler,
    LinearCongruentPseudorandomNumberGeneratorCommand
)


@click.group(name="linear_congruent_pseudorandom_number_generator")
def linear_congruent_pseudorandom_number_generator_group() -> None:
    ...


@linear_congruent_pseudorandom_number_generator_group.command(name="generate")
@click.option("-a", required=True, help="a number for generate sequence", type=int)
@click.option("-b", required=True, help="b number for generate sequence", type=int)
@click.option("-m", required=True, help="m number for generate sequence", type=int)
@click.option("-x0", required=True, help="x0 start number for generate sequence", type=int)
@click.option("-s", "--size", required=True, help="size of sequence", type=int, default=200)
def cmd_generate_handler(
        a: int,
        b: int,
        m: int,
        x0: int,
        size: int,
        interactor: FromDishka[LinearCongruentPseudorandomNumberGeneratorCommandHandler]
) -> None:
    command: LinearCongruentPseudorandomNumberGeneratorCommand = LinearCongruentPseudorandomNumberGeneratorCommand(
        a=a,
        b=b,
        m=m,
        x0=x0,
        size=size,
    )

    interactor(command)
