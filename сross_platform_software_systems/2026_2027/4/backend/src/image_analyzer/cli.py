from pathlib import Path

import click

from image_analyzer.application.training import train_and_save_model
from image_analyzer.config import default_artifact_path, resolve_dataset_dir
from image_analyzer.domain.types import TrainingConfig


@click.group()
def main() -> None:
    """CLI for training the shape classifier."""


@main.command("train")
@click.option(
    "--data-dir",
    type=click.Path(exists=False, file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Path to the dataset directory with class subfolders.",
)
@click.option(
    "--artifact-path",
    type=click.Path(file_okay=True, dir_okay=False, path_type=Path),
    default=default_artifact_path(),
    show_default=True,
    help="Where to save the trained model artifact.",
)
@click.option("--epochs", type=int, default=30, show_default=True)
@click.option("--batch-size", type=click.IntRange(min=1), default=32, show_default=True)
@click.option("--learning-rate", type=click.FloatRange(min=1e-8), default=1e-3, show_default=True)
@click.option("--hidden-size", type=click.IntRange(min=1), default=128, show_default=True)
@click.option("--test-size", type=click.FloatRange(min=0.01, max=0.99), default=0.2, show_default=True)
@click.option("--seed", type=int, default=42, show_default=True)
@click.option("--image-width", type=click.IntRange(min=1), default=20, show_default=True)
@click.option("--image-height", type=click.IntRange(min=1), default=20, show_default=True)
@click.option(
    "--device",
    type=click.Choice(["auto", "cpu", "cuda", "mps"], case_sensitive=False),
    default="auto",
    show_default=True,
)
def train_command(
    data_dir: Path | None,
    artifact_path: Path,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    hidden_size: int,
    test_size: float,
    seed: int,
    image_width: int,
    image_height: int,
    device: str,
) -> None:
    try:
        resolved_data_dir = resolve_dataset_dir(data_dir)
    except FileNotFoundError as error:
        raise click.ClickException(str(error)) from error

    config = TrainingConfig(
        data_dir=resolved_data_dir,
        artifact_path=artifact_path.expanduser().resolve(),
        epochs=epochs,
        batch_size=batch_size,
        learning_rate=learning_rate,
        hidden_size=hidden_size,
        test_size=test_size,
        seed=seed,
        image_width=image_width,
        image_height=image_height,
        device=device.lower(),
    )

    try:
        report = train_and_save_model(config)
    except (FileNotFoundError, ValueError) as error:
        raise click.ClickException(str(error)) from error

    click.echo(f"Dataset: {resolved_data_dir}")
    click.echo(f"Artifact: {report.artifact_path}")
    click.echo(f"Accuracy: {report.accuracy:.4f}")
    click.echo(f"Classes: {', '.join(report.class_names)}")
    click.echo(f"Train/Test samples: {report.train_samples}/{report.test_samples}")
    click.echo(f"Device: {report.device}")


if __name__ == "__main__":
    main()
