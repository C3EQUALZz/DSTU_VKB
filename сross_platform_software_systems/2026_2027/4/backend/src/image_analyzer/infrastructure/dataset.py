from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, UnidentifiedImageError

from image_analyzer.domain.constants import label_for_folder
from image_analyzer.domain.types import DatasetBundle


def preprocess_image_bytes(image_bytes: bytes, image_width: int, image_height: int) -> np.ndarray:
    try:
        image = Image.open(BytesIO(image_bytes)).convert("L")
    except UnidentifiedImageError as error:
        msg = "Uploaded file is not a supported image."
        raise ValueError(msg) from error

    image = image.resize((image_width, image_height))
    image_array = np.asarray(image, dtype=np.float32) / 255.0
    return image_array.flatten()


class ShapeDatasetLoader:
    def __init__(
        self,
        data_dir: Path,
        image_width: int,
        image_height: int,
        test_size: float,
        seed: int,
    ) -> None:
        self._data_dir = data_dir
        self._image_width = image_width
        self._image_height = image_height
        self._test_size = test_size
        self._seed = seed

    def load(self) -> DatasetBundle:
        features, labels, class_names = self._load_images()
        train_idx, test_idx = self._split_indices(labels)

        return DatasetBundle(
            train_features=features[train_idx].astype(np.float32),
            train_labels=labels[train_idx].astype(np.int64),
            test_features=features[test_idx].astype(np.float32),
            test_labels=labels[test_idx].astype(np.int64),
            class_names=class_names,
            image_width=self._image_width,
            image_height=self._image_height,
        )

    def _load_images(self) -> tuple[np.ndarray, np.ndarray, tuple[str, ...]]:
        if not self._data_dir.is_dir():
            msg = f"Dataset directory does not exist: {self._data_dir}"
            raise FileNotFoundError(msg)

        feature_rows: list[np.ndarray] = []
        label_rows: list[int] = []
        class_names: list[str] = []

        for folder_path in sorted(self._data_dir.iterdir()):
            if not folder_path.is_dir():
                continue

            folder_features: list[np.ndarray] = []

            for image_path in sorted(folder_path.iterdir()):
                if not image_path.is_file():
                    continue
                try:
                    folder_features.append(
                        preprocess_image_bytes(
                            image_path.read_bytes(),
                            image_width=self._image_width,
                            image_height=self._image_height,
                        ),
                    )
                except (OSError, ValueError, UnidentifiedImageError):
                    continue

            if not folder_features:
                continue

            class_index = len(class_names)
            class_names.append(label_for_folder(folder_path.name))
            feature_rows.extend(folder_features)
            label_rows.extend([class_index] * len(folder_features))

        if len(class_names) < 2:
            msg = f"Expected at least 2 classes in dataset directory: {self._data_dir}"
            raise ValueError(msg)

        if not feature_rows:
            msg = f"Dataset directory is empty or contains unreadable images: {self._data_dir}"
            raise ValueError(msg)

        return (
            np.asarray(feature_rows, dtype=np.float32),
            np.asarray(label_rows, dtype=np.int64),
            tuple(class_names),
        )

    def _split_indices(self, labels: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        rng = np.random.default_rng(self._seed)
        train_indices: list[np.ndarray] = []
        test_indices: list[np.ndarray] = []

        for class_index in np.unique(labels):
            class_indices = np.flatnonzero(labels == class_index)
            rng.shuffle(class_indices)

            if len(class_indices) < 2:
                msg = f"Class {class_index} must contain at least two images."
                raise ValueError(msg)

            raw_test_count = int(round(len(class_indices) * self._test_size))
            test_count = min(max(raw_test_count, 1), len(class_indices) - 1)
            split_at = len(class_indices) - test_count

            train_indices.append(class_indices[:split_at])
            test_indices.append(class_indices[split_at:])

        train_idx = np.concatenate(train_indices)
        test_idx = np.concatenate(test_indices)
        rng.shuffle(train_idx)
        rng.shuffle(test_idx)
        return train_idx, test_idx
