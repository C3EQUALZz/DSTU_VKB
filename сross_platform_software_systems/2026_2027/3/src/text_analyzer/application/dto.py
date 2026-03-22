from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class TrainingConfig:
    embedding_dim: int = 64
    hidden_dim: int = 128
    num_layers: int = 2
    dropout: float = 0.3
    max_vocab_size: int = 40000
    max_seq_length: int = 500
    batch_size: int = 64
    epochs: int = 30
    learning_rate: float = 0.003
    test_ratio: float = 0.2


@dataclass(frozen=True, slots=True, kw_only=True)
class TrainingResult:
    train_losses: list[float]
    val_losses: list[float]
    val_accuracies: list[float]
    best_val_accuracy: float
    best_epoch: int


@dataclass(frozen=True, slots=True, kw_only=True)
class EvaluationResult:
    accuracy: float
    loss: float
    total_samples: int
    correct_predictions: int
