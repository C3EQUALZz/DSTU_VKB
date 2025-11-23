"""Main CLI entry point."""

from theory_of_pseudorandom_generators.presentation.cli.linear_congruent_pseudorandom_number_generator import (
    LinearCongruentGeneratorCommands,
)


def main() -> None:
    """Main entry point for CLI."""
    commands = LinearCongruentGeneratorCommands()
    commands.run()


if __name__ == "__main__":
    main()

