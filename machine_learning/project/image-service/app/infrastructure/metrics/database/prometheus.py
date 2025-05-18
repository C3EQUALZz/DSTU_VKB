from typing import override

from prometheus_client import CollectorRegistry, Histogram

from app.infrastructure.metrics.database.base import BaseDatabaseMetricsMixin


class PrometheusDatabaseMixin(BaseDatabaseMetricsMixin):
    def __init__(self, registry: CollectorRegistry) -> None:
        self._db_query_latency = Histogram(
            "db_query_duration_seconds",
            "Database query latency by query name",
            ["query"],
            registry=registry
        )

    @override
    def observe_db_query_latency(self, query: str, latency: float) -> None:
        self._db_query_latency.labels(query=query).observe(latency)
