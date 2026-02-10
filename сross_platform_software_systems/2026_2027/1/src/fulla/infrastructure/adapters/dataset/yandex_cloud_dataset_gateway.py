import logging
import zipfile
from pathlib import Path
from typing import Final, final

import gdown
import numpy as np
import numpy.typing as npt
from PIL import Image, UnidentifiedImageError
from sklearn.model_selection import train_test_split

from fulla.domain.shape_recognition.value_objects.dataset import PreparedDataset

logger: Final[logging.Logger] = logging.getLogger(__name__)

# Mapping: folder name → class index
#   '0' → 0 (triangle), '3' → 1 (circle), else → 2 (square)
_CLASS_NAMES: Final[dict[int, str]] = {0: "Круг", 1: "Треугольник", 2: "Квадрат"}


@final
class YandexCloudDatasetGateway:
    """Downloads hw_light.zip from Yandex Cloud, loads images and splits train/test."""

    def __init__(
        self,
        dataset_url: str,
        data_dir: str,
        img_height: int,
        img_width: int,
        test_size: float,
        random_state: int,
    ) -> None:
        self._dataset_url: Final[str] = dataset_url
        self._data_dir: Final[Path] = Path(data_dir)
        self._img_height: Final[int] = img_height
        self._img_width: Final[int] = img_width
        self._test_size: Final[float] = test_size
        self._random_state: Final[int] = random_state
        self._cache: PreparedDataset | None = None

    def load(self) -> PreparedDataset:
        if self._cache is not None:
            return self._cache

        self._ensure_downloaded()
        x_all, y_all = self._load_images()

        x_train, x_test, y_train, y_test = train_test_split(
            x_all,
            y_all,
            test_size=self._test_size,
            random_state=self._random_state,
        )

        self._cache = PreparedDataset(
            x_train=x_train.astype(np.float32),
            y_train=y_train,
            x_test=x_test.astype(np.float32),
            y_test=y_test,
        )

        logger.info(
            "Dataset loaded: %d train, %d test samples (input_size=%d)",
            self._cache.train_count,
            self._cache.test_count,
            self._cache.input_size,
        )

        return self._cache

    def _ensure_downloaded(self) -> None:
        zip_path = Path(f"{self._data_dir}.zip")

        if self._data_dir.is_dir():
            logger.debug("Dataset directory already exists: %s", self._data_dir)
            return

        if not zip_path.is_file():
            logger.info("Downloading dataset from %s", self._dataset_url)
            gdown.download(self._dataset_url, str(zip_path), quiet=False)

        logger.info("Extracting archive %s", zip_path)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(".")

    def _load_images(self) -> tuple[npt.NDArray[np.float32], npt.NDArray[np.intp]]:
        x_data: list[npt.NDArray[np.float32]] = []
        y_data: list[int] = []

        for folder_path in sorted(self._data_dir.iterdir()):
            if not folder_path.is_dir():
                continue

            for img_path in folder_path.iterdir():
                try:
                    img: Image.Image = Image.open(img_path).convert("L")
                    img = img.resize((self._img_width, self._img_height))
                    img_arr: npt.NDArray[np.float32] = np.array(img, dtype=np.float32) / 255.0
                    x_data.append(img_arr.flatten())
                except (OSError, UnidentifiedImageError):
                    logger.warning("Failed to load image: %s", img_path)
                    continue

                if folder_path.name == "0":
                    y_data.append(0)
                elif folder_path.name == "3":
                    y_data.append(1)
                else:
                    y_data.append(2)

        logger.info("Loaded %d images across %s classes", len(x_data), _CLASS_NAMES)
        return np.array(x_data, dtype=np.float32), np.array(y_data)
