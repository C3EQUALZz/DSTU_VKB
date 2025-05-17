import logging
import os
from pathlib import Path
from tempfile import gettempdir
from typing import Optional, Any

from prometheus_client import Counter, Histogram, CollectorRegistry
from taskiq.abc.middleware import TaskiqMiddleware
from taskiq.message import TaskiqMessage
from taskiq.result import TaskiqResult

logger = logging.getLogger(__name__)


class PrometheusWithRegistryMiddleware(TaskiqMiddleware):
    """
    Middleware для сбора метрик Taskiq с использованием общего CollectorRegistry.
    Не запускает отдельный HTTP-сервер.
    """

    def __init__(
            self,
            registry: Optional[CollectorRegistry] = None,
            metrics_path: Optional[Path] = None,
    ) -> None:
        super().__init__()
        self.registry = registry or CollectorRegistry()
        metrics_path = metrics_path or Path(gettempdir()) / "taskiq_worker"

        if not metrics_path.exists():
            metrics_path.mkdir(parents=True)

        logger.debug(f"Setting up multiproc dir to {metrics_path}")
        os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(metrics_path)

        logger.debug("Initializing metrics")
        try:
            # Метрики инициализируются с использованием общего реестра
            self.found_errors = Counter(
                "taskiq_found_errors_total",
                "Number of found errors",
                ["task_name"],
                registry=self.registry
            )
            self.received_tasks = Counter(
                "taskiq_received_tasks_total",
                "Number of received tasks",
                ["task_name"],
                registry=self.registry
            )
            self.success_tasks = Counter(
                "taskiq_success_tasks_total",
                "Number of successfully executed tasks",
                ["task_name"],
                registry=self.registry
            )
            self.saved_results = Counter(
                "taskiq_saved_results_total",
                "Number of saved results in result backend",
                ["task_name"],
                registry=self.registry
            )
            self.execution_time = Histogram(
                "taskiq_execution_time_seconds",
                "Time of function execution",
                ["task_name"],
                registry=self.registry
            )
        except ImportError as exc:
            raise ImportError(
                "Cannot initialize metrics. Please install 'taskiq[metrics]'.",
            ) from exc

    def startup(self) -> None:
        """
        Просто проверяем, что registry существует.
        Запуск HTTP-сервера теперь выполняется в основном приложении.
        """
        if not self.broker.is_worker_process:
            return
        logger.debug("Prometheus middleware started without HTTP server")

    def pre_execute(
            self,
            message: TaskiqMessage,
    ) -> TaskiqMessage:
        """
        Отслеживаем полученные задачи.
        """
        self.received_tasks.labels(message.task_name).inc()
        return message

    def post_execute(
            self,
            message: TaskiqMessage,
            result: TaskiqResult[Any],
    ) -> None:
        """
        Отслеживаем ошибки и успешные выполнения.
        """
        if result.is_err:
            self.found_errors.labels(message.task_name).inc()
        else:
            self.success_tasks.labels(message.task_name).inc()
        self.execution_time.labels(message.task_name).observe(result.execution_time)

    def post_save(
            self,
            message: TaskiqMessage,
            result: TaskiqResult[Any],
    ) -> None:
        """
        Отслеживаем сохранение результатов.
        """
        self.saved_results.labels(message.task_name).inc()
