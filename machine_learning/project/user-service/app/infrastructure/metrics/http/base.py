from abc import abstractmethod, ABC


class BaseHTTPMetricsMixin(ABC):
    @abstractmethod
    def increment_http_requests(self, method: str, endpoint: str, status_code: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def observe_http_latency(self, method: str, endpoint: str, latency: float) -> None:
        raise NotImplementedError
