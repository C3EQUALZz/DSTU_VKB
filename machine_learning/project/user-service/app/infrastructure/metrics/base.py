from abc import ABC, abstractmethod
from typing import Callable

from app.infrastructure.metrics.database.base import BaseDatabaseMetricsMixin
from app.infrastructure.metrics.http.base import BaseHTTPMetricsMixin


class BaseMetricsClient(BaseHTTPMetricsMixin, BaseDatabaseMetricsMixin, ABC):
    """Абстракция для работы с метриками"""

    @abstractmethod
    def make_app(self) -> Callable[..., ...]:
        raise NotImplementedError

    @abstractmethod
    def generate_latest(self) -> bytes:
        raise NotImplementedError
