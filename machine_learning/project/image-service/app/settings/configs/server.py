from pathlib import Path
from typing import Final

from gunicorn.arbiter import Arbiter
from gunicorn.workers.base import Worker
from prometheus_client import multiprocess

from app.settings.configs.app import Settings, get_settings

settings: Final[Settings] = get_settings()

bind: Final[str] = settings.server.bind

workers: Final[int] = settings.server.workers
max_requests: Final[int] = settings.server.max_requests
max_requests_jitter: Final[int] = settings.server.max_jitter
worker_class: Final[str] = settings.server.worker_class
log_level: Final[str] = settings.server.log_level
log_file: Final[str] = settings.server.log_file


def post_fork(server: Arbiter, worker: Worker) -> None:
    worker.log.info('[post_fork] age: %s. pid: %s', worker.age, worker.pid)

    if settings.server.multiprocess_dir is None:
        return

    try:
        import prometheus_client
    except ImportError:
        worker.log.error(
            "[post_fork] age: %s. pid: %s. Can't import prometheus_client",
            worker.age,
            worker.pid,
        )
        return

    try:
        import filelock
    except ImportError:
        worker.log.error(
            "[post_fork] age: %s. pid: %s. Can't import filelock",
            worker.age,
            worker.pid,
        )
        return

    worker_id = None
    for idx in range(0, server.num_workers):
        worker_id_potential = idx + 1
        worker_id_lock_file = f'worker_id_{worker_id_potential}.lock'
        try:
            worker_id_lock = filelock.FileLock(
                lock_file=worker_id_lock_file,
            ).acquire(blocking=False)
        except filelock.Timeout:
            worker.log.info(
                "[post_fork] age: %s. pid: %s. worker_id %s is locked",
                worker.age,
                worker.pid,
                worker_id_potential,
            )
        else:
            worker_id = worker_id_potential
            # необходимо сохранить ссылку на worker_id_lock,
            # чтобы после выхода из области видимости функции
            # не был вызван метод __del__ у этого объекта
            #
            # метод __del__ вызывает release, причем c force=True
            setattr(worker, 'worker_id', worker_id)
            setattr(worker, 'worker_id_lock', worker_id_lock)
            break

    if not worker_id:
        worker.log.error(
            "[post_fork] age: %s. pid: %s. There is no worker_id",
            worker.age,
            worker.pid,
        )
        return

    # noinspection PyUnresolvedReferences
    prometheus_client.values.ValueClass = prometheus_client.values.MultiProcessValue(
        process_identifier=lambda: worker_id,
    )

    worker.log.info(
        '[post_fork] age: %s. pid: %s. Lock worker_id %s',
        worker.age,
        worker.pid,
        worker_id,
    )


def post_worker_init(worker: Worker) -> None:
    worker.log.info(
        '[post_worker_init] age: %s. pid: %s. worker_id: %s',
        worker.age,
        worker.pid,
        getattr(worker, 'worker_id', None),
    )


def when_ready(server: Arbiter) -> None:
    server.log.info("Server is ready. Spawning workers")


def child_exit(server: Arbiter, worker: Worker) -> None:
    multiprocess.mark_process_dead(worker.pid)
