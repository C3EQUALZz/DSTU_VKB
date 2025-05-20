from typing import override, Final

from prometheus_client import CollectorRegistry, Histogram

from app.infrastructure.metrics.database.base import BaseDatabaseMetricsMixin


class PrometheusDatabaseMixin(BaseDatabaseMetricsMixin):
    def __init__(self, registry: CollectorRegistry, service_name: str) -> None:
        self._db_query_latency: Final[Histogram] = Histogram(
            "db_query_duration_seconds",
            "Database query latency by query name",
            ["query", "service"],
            registry=registry
        )

        self._service_name: Final[str] = service_name

    @override
    def observe_db_query_latency(self, query: str, latency: float) -> None:
        self._db_query_latency.labels(
            service=self._service_name,
            query=query
        ).observe(latency)
