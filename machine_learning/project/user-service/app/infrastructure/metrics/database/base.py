from abc import ABC, abstractmethod


class BaseDatabaseMetricsMixin(ABC):
    @abstractmethod
    def observe_db_query_latency(self, query: str, latency: float) -> None:
        raise NotImplementedError
