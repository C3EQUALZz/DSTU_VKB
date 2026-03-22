import logging
from pathlib import Path
from typing import Final

import click
from dishka import FromDishka
from dishka.integrations.click import inject, setup_dishka

from text_analyzer.application.commands.download_dataset import (
    DownloadDatasetCommand,
    DownloadDatasetCommandHandler,
)
from text_analyzer.application.commands.evaluate_model import (
    EvaluateModelCommand,
    EvaluateModelCommandHandler,
)
from text_analyzer.application.commands.predict import (
    PredictCommand,
    PredictCommandHandler,
)
from text_analyzer.application.commands.train_model import (
    TrainModelCommand,
    TrainModelCommandHandler,
)
from text_analyzer.application.commands.visualize import (
    VisualizeCommand,
    VisualizeCommandHandler,
)
from text_analyzer.application.dto import TrainingConfig
from text_analyzer.setup.container import create_container

_DATASET_URL: Final[str] = (
    "https://storage.yandexcloud.net/aiueducation/Content/base/l7/tesla.zip"
)
_DEFAULT_DATA_DIR: Final[str] = "data"
_DEFAULT_MODEL_DIR: Final[str] = "output"


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging.")
@click.pass_context
def cli(ctx: click.Context, *, verbose: bool) -> None:
    """Tesla review sentiment classifier — Lab #3."""
    _setup_logging(verbose)
    container = create_container()
    setup_dishka(container=container, context=ctx, auto_inject=True)


@cli.command()
@click.option("--url", default=_DATASET_URL, help="Dataset archive URL.")
@click.option("--output", "-o", default=_DEFAULT_DATA_DIR, help="Output directory.")
@inject
def download(
    url: str,
    output: str,
    handler: FromDishka[DownloadDatasetCommandHandler],
) -> None:
    """Download and extract the Tesla reviews dataset."""
    result = handler(DownloadDatasetCommand(url=url, output_dir=Path(output)))
    click.echo(f"Dataset ready at: {result}")


@cli.command()
@click.option("--data-dir", "-d", default=_DEFAULT_DATA_DIR, help="Dataset directory.")
@click.option("--model-dir", "-m", default=_DEFAULT_MODEL_DIR, help="Model output directory.")
@click.option("--epochs", default=30, help="Number of training epochs.")
@click.option("--batch-size", default=64, help="Batch size.")
@click.option("--lr", default=0.003, type=float, help="Learning rate.")
@click.option("--max-vocab", default=40000, help="Maximum vocabulary size.")
@click.option("--max-seq-len", default=500, help="Maximum sequence length.")
@click.option("--hidden-dim", default=128, help="Hidden layer dimension.")
@inject
def train(
    data_dir: str,
    model_dir: str,
    epochs: int,
    batch_size: int,
    lr: float,
    max_vocab: int,
    max_seq_len: int,
    hidden_dim: int,
    handler: FromDishka[TrainModelCommandHandler],
) -> None:
    """Train the sentiment classification model."""
    config = TrainingConfig(
        epochs=epochs,
        batch_size=batch_size,
        learning_rate=lr,
        max_vocab_size=max_vocab,
        max_seq_length=max_seq_len,
        hidden_dim=hidden_dim,
    )

    result = handler(TrainModelCommand(
        data_dir=Path(data_dir),
        model_output_dir=Path(model_dir),
        config=config,
    ))

    click.echo("\n=== Training Results ===")
    click.echo(f"Best validation accuracy: {result.best_val_accuracy * 100:.2f}%")
    click.echo(f"Best epoch: {result.best_epoch}")
    click.echo(f"Final train loss: {result.train_losses[-1]:.4f}")
    click.echo(f"Final val loss: {result.val_losses[-1]:.4f}")


@cli.command()
@click.option("--data-dir", "-d", default=_DEFAULT_DATA_DIR, help="Dataset directory.")
@click.option("--model-dir", "-m", default=_DEFAULT_MODEL_DIR, help="Model directory.")
@inject
def evaluate(
    data_dir: str,
    model_dir: str,
    handler: FromDishka[EvaluateModelCommandHandler],
) -> None:
    """Evaluate a trained model on the test set."""
    config = TrainingConfig()
    result = handler(EvaluateModelCommand(
        data_dir=Path(data_dir),
        model_dir=Path(model_dir),
        config=config,
    ))

    click.echo("\n=== Evaluation Results ===")
    click.echo(f"Accuracy: {result.accuracy * 100:.2f}%")
    click.echo(f"Loss: {result.loss:.4f}")
    click.echo(f"Correct: {result.correct_predictions}/{result.total_samples}")


@cli.command()
@click.option("--text", "-t", required=True, help="Review text to classify.")
@click.option("--model-dir", "-m", default=_DEFAULT_MODEL_DIR, help="Model directory.")
@inject
def predict(
    text: str,
    model_dir: str,
    handler: FromDishka[PredictCommandHandler],
) -> None:
    """Classify a single review as positive or negative."""
    config = TrainingConfig()
    result = handler(PredictCommand(
        text=text,
        model_dir=Path(model_dir),
        config=config,
    ))

    label = "Позитивный" if result.sentiment.value == "positive" else "Негативный"
    click.echo(f"\nТекст: {result.text}")
    click.echo(f"Результат: {label} ({result.sentiment.value})")


@cli.command()
@click.option("--url", default=_DATASET_URL, help="Dataset archive URL.")
@click.option("--data-dir", "-d", default=_DEFAULT_DATA_DIR, help="Dataset directory.")
@click.option("--model-dir", "-m", default=_DEFAULT_MODEL_DIR, help="Model output directory.")
@click.option("--epochs", default=30, help="Number of training epochs.")
@inject
def pipeline(
    url: str,
    data_dir: str,
    model_dir: str,
    epochs: int,
    download_handler: FromDishka[DownloadDatasetCommandHandler],
    train_handler: FromDishka[TrainModelCommandHandler],
) -> None:
    """Run the full pipeline: download -> train."""
    config = TrainingConfig(epochs=epochs)

    click.echo("Step 1/2: Downloading dataset...")
    download_handler(DownloadDatasetCommand(url=url, output_dir=Path(data_dir)))
    click.echo("Dataset ready.\n")

    click.echo("Step 2/2: Training model...")
    result = train_handler(TrainModelCommand(
        data_dir=Path(data_dir),
        model_output_dir=Path(model_dir),
        config=config,
    ))

    click.echo("\n=== Pipeline Complete ===")
    click.echo(f"Best validation accuracy: {result.best_val_accuracy * 100:.2f}%")
    click.echo(f"Best epoch: {result.best_epoch}")


@cli.command()
@click.option("--data-dir", "-d", default=_DEFAULT_DATA_DIR, help="Dataset directory.")
@click.option("--model-dir", "-m", default=_DEFAULT_MODEL_DIR, help="Model directory.")
@click.option("--output-dir", "-o", default="plots", help="Directory for saving plots.")
@click.option("--epochs", default=30, help="Number of training epochs.")
@inject
def visualize(
    data_dir: str,
    model_dir: str,
    output_dir: str,
    epochs: int,
    handler: FromDishka[VisualizeCommandHandler],
) -> None:
    """Generate training and dataset analysis plots."""
    config = TrainingConfig(epochs=epochs)
    plots = handler(VisualizeCommand(
        data_dir=Path(data_dir),
        model_dir=Path(model_dir),
        output_dir=Path(output_dir),
        config=config,
    ))

    click.echo(f"\n=== Generated {len(plots)} plots ===")
    for p in plots:
        click.echo(f"  {p}")
