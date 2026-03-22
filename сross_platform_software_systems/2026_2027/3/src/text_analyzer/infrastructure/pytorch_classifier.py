import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Final, final

import torch
from torch import Tensor, nn
from torch.utils.data import DataLoader, TensorDataset

from text_analyzer.application.dto import EvaluationResult, TrainingConfig, TrainingResult

logger: Final[logging.Logger] = logging.getLogger(__name__)


class SentimentNet(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, dropout: float) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.net(x).squeeze(-1)


@final
class PytorchSentimentClassifier:
    def __init__(self) -> None:
        self._model: SentimentNet | None = None
        self._idf: Tensor | None = None
        self._device: torch.device = torch.device(
            "mps" if torch.backends.mps.is_available()
            else "cuda" if torch.cuda.is_available()
            else "cpu"
        )

    def fit(
        self,
        train_sequences: Sequence[Sequence[int]],
        train_labels: Sequence[int],
        val_sequences: Sequence[Sequence[int]],
        val_labels: Sequence[int],
        vocab_size: int,
        config: TrainingConfig,
    ) -> TrainingResult:
        train_bow = self._sequences_to_bow(train_sequences, vocab_size)
        self._idf = self._compute_idf(train_bow)
        train_features = self._apply_tfidf(train_bow, self._idf)

        val_bow = self._sequences_to_bow(val_sequences, vocab_size)
        val_features = self._apply_tfidf(val_bow, self._idf)

        logger.info("TF-IDF features: dim=%d, train=%d, val=%d", vocab_size, len(train_labels), len(val_labels))

        self._model = SentimentNet(
            input_dim=vocab_size,
            hidden_dim=config.hidden_dim,
            dropout=config.dropout,
        ).to(self._device)

        param_count = sum(p.numel() for p in self._model.parameters() if p.requires_grad)
        logger.info("Model parameters: %d", param_count)

        train_loader = self._create_feature_dataloader(train_features, train_labels, config.batch_size, shuffle=True)
        val_loader = self._create_feature_dataloader(val_features, val_labels, config.batch_size, shuffle=False)

        criterion = nn.BCEWithLogitsLoss()
        optimizer = torch.optim.AdamW(
            self._model.parameters(),
            lr=config.learning_rate,
            weight_decay=1e-2,
        )
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=config.epochs, eta_min=1e-5,
        )

        train_losses: list[float] = []
        val_losses: list[float] = []
        val_accuracies: list[float] = []
        best_val_accuracy = 0.0
        best_epoch = 0
        best_state: dict[str, Tensor] = {}

        logger.info("Training on device: %s", self._device)

        for epoch in range(config.epochs):
            train_loss = self._train_epoch(train_loader, criterion, optimizer)
            val_loss, val_acc = self._evaluate_epoch(val_loader, criterion)

            scheduler.step()

            train_losses.append(train_loss)
            val_losses.append(val_loss)
            val_accuracies.append(val_acc)

            if val_acc > best_val_accuracy:
                best_val_accuracy = val_acc
                best_epoch = epoch + 1
                best_state = {k: v.clone() for k, v in self._model.state_dict().items()}

            current_lr = optimizer.param_groups[0]["lr"]
            logger.info(
                "Epoch %d/%d — train_loss: %.4f, val_loss: %.4f, val_acc: %.2f%%, lr: %.6f",
                epoch + 1, config.epochs, train_loss, val_loss, val_acc * 100, current_lr,
            )

        if best_state:
            self._model.load_state_dict(best_state)

        return TrainingResult(
            train_losses=train_losses,
            val_losses=val_losses,
            val_accuracies=val_accuracies,
            best_val_accuracy=best_val_accuracy,
            best_epoch=best_epoch,
        )

    def evaluate(
        self,
        sequences: Sequence[Sequence[int]],
        labels: Sequence[int],
    ) -> EvaluationResult:
        if self._model is None or self._idf is None:
            msg = "Model is not trained or loaded"
            raise RuntimeError(msg)

        bow = self._sequences_to_bow(sequences, self._idf.size(0))
        features = self._apply_tfidf(bow, self._idf.cpu())
        loader = self._create_feature_dataloader(features, labels, batch_size=64, shuffle=False)
        criterion = nn.BCEWithLogitsLoss()
        loss, accuracy = self._evaluate_epoch(loader, criterion)
        total = len(labels)
        correct = int(accuracy * total)

        return EvaluationResult(
            accuracy=accuracy,
            loss=loss,
            total_samples=total,
            correct_predictions=correct,
        )

    def predict(self, sequences: Sequence[Sequence[int]]) -> list[int]:
        if self._model is None or self._idf is None:
            msg = "Model is not trained or loaded"
            raise RuntimeError(msg)

        bow = self._sequences_to_bow(sequences, self._idf.size(0))
        features = self._apply_tfidf(bow, self._idf.cpu())

        self._model.eval()
        with torch.no_grad():
            output = self._model(features.to(self._device))
            preds = (torch.sigmoid(output) >= 0.5).int().cpu().tolist()
        return preds

    def save_model(self, path: Path) -> None:
        if self._model is None or self._idf is None:
            msg = "No model to save"
            raise RuntimeError(msg)
        torch.save({"model": self._model.state_dict(), "idf": self._idf}, path)
        logger.info("Model saved to %s", path)

    def load_model(self, path: Path, vocab_size: int, config: TrainingConfig) -> None:
        checkpoint = torch.load(path, map_location=self._device, weights_only=True)
        self._idf = checkpoint["idf"]
        self._model = SentimentNet(
            input_dim=vocab_size,
            hidden_dim=config.hidden_dim,
            dropout=config.dropout,
        ).to(self._device)
        self._model.load_state_dict(checkpoint["model"])
        self._model.eval()
        logger.info("Model loaded from %s", path)

    @staticmethod
    def _sequences_to_bow(sequences: Sequence[Sequence[int]], vocab_size: int) -> Tensor:
        n = len(sequences)
        bow = torch.zeros(n, vocab_size)
        for i, seq in enumerate(sequences):
            for idx in seq:
                if 0 < idx < vocab_size:
                    bow[i][idx] += 1.0
        return bow

    @staticmethod
    def _compute_idf(bow: Tensor) -> Tensor:
        n_docs = bow.size(0)
        df = (bow > 0).float().sum(dim=0)
        return torch.log(torch.tensor(n_docs + 1.0) / (df + 1.0)) + 1.0

    @staticmethod
    def _apply_tfidf(bow: Tensor, idf: Tensor) -> Tensor:
        tf = bow
        tfidf = tf * idf
        norms = tfidf.norm(dim=1, keepdim=True).clamp(min=1e-8)
        return tfidf / norms

    def _train_epoch(
        self,
        loader: DataLoader[tuple[Tensor, ...]],
        criterion: nn.Module,
        optimizer: torch.optim.Optimizer,
    ) -> float:
        assert self._model is not None
        self._model.train()
        total_loss = 0.0
        batches = 0

        for batch_x, batch_y in loader:
            batch_x = batch_x.to(self._device)
            batch_y = batch_y.to(self._device)

            optimizer.zero_grad()
            output = self._model(batch_x)
            loss = criterion(output, batch_y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            batches += 1

        return total_loss / max(batches, 1)

    def _evaluate_epoch(
        self,
        loader: DataLoader[tuple[Tensor, ...]],
        criterion: nn.Module,
    ) -> tuple[float, float]:
        assert self._model is not None
        self._model.eval()
        total_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for batch_x, batch_y in loader:
                batch_x = batch_x.to(self._device)
                batch_y = batch_y.to(self._device)

                output = self._model(batch_x)
                loss = criterion(output, batch_y)

                total_loss += loss.item()
                predictions = (torch.sigmoid(output) >= 0.5).float()
                correct += (predictions == batch_y).sum().item()
                total += batch_y.size(0)

        avg_loss = total_loss / max(len(loader), 1)
        accuracy = correct / max(total, 1)
        return avg_loss, accuracy

    @staticmethod
    def _create_feature_dataloader(
        features: Tensor,
        labels: Sequence[int],
        batch_size: int,
        *,
        shuffle: bool,
    ) -> DataLoader[tuple[Tensor, ...]]:
        y_tensor = torch.tensor(list(labels), dtype=torch.float32)
        dataset = TensorDataset(features, y_tensor)
        return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
