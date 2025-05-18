from typing import override, Final

from prometheus_client import CollectorRegistry, Counter, Histogram

from app.infrastructure.metrics.http.base import BaseHTTPMetricsMixin


class PrometheusHTTPMixin(BaseHTTPMetricsMixin):
    def __init__(self, registry: CollectorRegistry) -> None:
        self._http_requests_counter: Final[Counter] = Counter(
            "http_requests_total",
            "Total HTTP requests by method, endpoint and status code",
            ["method", "endpoint", "status_code"],
            registry=registry
        )
        self._http_latency_histogram: Final[Histogram] = Histogram(
            "http_request_duration_seconds",
            "HTTP request latency by method and endpoint",
            ["method", "endpoint"],
            registry=registry
        )

    @override
    def increment_http_requests(self, method: str, endpoint: str, status_code: int) -> None:
        self._http_requests_counter.labels(method=method, endpoint=endpoint, status_code=status_code).inc()

    @override
    def observe_http_latency(self, method: str, endpoint: str, latency: float) -> None:
        self._http_latency_histogram.labels(method=method, endpoint=endpoint).observe(latency)
