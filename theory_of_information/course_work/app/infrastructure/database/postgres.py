import logging
import subprocess
import sys
from dataclasses import dataclass
from datetime import (
    datetime,
    UTC,
)
from pathlib import Path
from subprocess import Popen

from app.application.cli.const import BACKUP_DIRECTORY_PATH
from app.infrastructure.database.base import BaseDatabaseCLIService
from typing_extensions import override


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PostgresConfig:
    user: str
    password: str
    host: str
    port: int
    database_name: str


class PostgresCLIService(BaseDatabaseCLIService):
    def __init__(
        self,
        psql_bin_path: Path,
        postgres_config: PostgresConfig,
    ) -> None:
        self._psql_bin_path = psql_bin_path
        self._config = postgres_config

    @override
    def list_all_databases(self) -> None:
        if sys.platform == "win32":
            psql_path: Path = self._psql_bin_path / "psql.exe"
        else:
            psql_path = self._psql_bin_path / "psql"

        process: Popen[bytes] = subprocess.Popen(
            [
                str(psql_path),
                "--dbname=postgresql://{}:{}@{}:{}/{}".format(
                    self._config.user,
                    self._config.password,
                    self._config.host,
                    self._config.port,
                    self._config.database_name,
                ),
                "--list",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output: bytes = process.communicate()[0]

        if int(process.returncode) != 0:
            logger.error("Command failed. Return code : %s", process.returncode)
            return

        for line in output.splitlines():
            print(line.decode())

    @override
    def create_backup(self) -> None:
        if sys.platform == "win32":
            psql_path: Path = self._psql_bin_path / "pg_dump.exe"
        else:
            psql_path: Path = self._psql_bin_path / "pg_dump"

        dest_file: Path = BACKUP_DIRECTORY_PATH / f"backup-{datetime.now(UTC).date()}.dump"

        process: Popen[bytes] = subprocess.Popen(
            [
                str(psql_path),
                "--dbname=postgresql://{}:{}@{}:{}/{}".format(
                    self._config.user,
                    self._config.password,
                    self._config.host,
                    self._config.port,
                    self._config.database_name,
                ),
                "-Fc",
                "-f",
                dest_file,
                "-v",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output, error = process.communicate()

        if int(process.returncode) != 0:
            logger.error("Command failed. Return code : {}".format(process.returncode))
            logger.error("Error output:", error.decode("utf-8"))
            return

        for line in output.splitlines():
            print(line.decode())
