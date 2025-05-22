from typing import Callable, Final, override

from prometheus_client import CollectorRegistry, make_asgi_app as prometheus_make_app, generate_latest

from app.infrastructure.metrics.base import BaseMetricsClient
from app.infrastructure.metrics.database.prometheus import PrometheusDatabaseMixin
from app.infrastructure.metrics.http.prometheus import PrometheusHTTPMixin


class PrometheusMetricsClient(
    PrometheusHTTPMixin,
    PrometheusDatabaseMixin,
    BaseMetricsClient
):
    def __init__(self, registry: CollectorRegistry, service_name: str) -> None:
        self._registry: Final[CollectorRegistry] = registry
        PrometheusHTTPMixin.__init__(self, registry=registry, service_name=service_name)
        PrometheusDatabaseMixin.__init__(self, registry=registry, service_name=service_name)

    @override
    def make_app(self) -> Callable[..., ...]:
        return prometheus_make_app(registry=self._registry)

    @override
    def generate_latest(self) -> bytes:
        return generate_latest(self._registry)