import logging
import subprocess
import sys
from dataclasses import dataclass
from datetime import (
    UTC,
    datetime,
)
from pathlib import Path
from subprocess import Popen

from typing_extensions import override

from app.application.cli.const import BACKUP_DIRECTORY_PATH
from app.infrastructure.database.base import BaseDatabaseCLIService

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PostgresConfig:
    """
    DTO class for getting postgres config.
    """
    user: str
    password: str
    host: str
    port: int
    database_name: str


class PostgresCLIService(BaseDatabaseCLIService):
    """
    CLI service for communication with Postgres.
    This service requires PostgreSQL to be installed on PC or server.
    """
    def __init__(
        self,
        psql_bin_path: Path,
        postgres_config: PostgresConfig,
    ) -> None:
        """
        :param psql_bin_path: Path to the psql binary.
        :param postgres_config: Postgres configuration, please see the DTO (PostgresConfig).
        """
        self._psql_bin_path = psql_bin_path
        self._config = postgres_config

    @override
    def list_all_databases(self) -> None:
        """
        This method prints all databases that are available by the config that user provides.
        """
        if sys.platform == "win32":
            psql_path: Path = self._psql_bin_path / "psql.exe"
        else:
            psql_path: Path = self._psql_bin_path / "psql"

        process: Popen[bytes] = subprocess.Popen(
            [
                str(psql_path),
                f"--dbname=postgresql://{self._config.user}:{self._config.password}@{self._config.host}:{self._config.port}/{self._config.database_name}",
                "--list",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output, error = process.communicate()

        if int(process.returncode) != 0:
            logger.error("Command failed. Return code : %s", process.returncode)
            logger.error("Error output:", error.decode("utf-8"))
            return

        for line in output.splitlines():
            print(line.decode("utf-8"))

    @override
    def create_backup(self) -> None:
        """
        This method creates a backup of the current database.
        Backup will be created at tmp directory. At the root of this project.
        """
        if sys.platform == "win32":
            psql_path: Path = self._psql_bin_path / "pg_dump.exe"
        else:
            psql_path: Path = self._psql_bin_path / "pg_dump"

        dest_file: Path = BACKUP_DIRECTORY_PATH / f"backup-{datetime.now(UTC).date()}.dump"

        process: Popen[bytes] = subprocess.Popen(
            [
                str(psql_path),
                f"--dbname=postgresql://{self._config.user}:{self._config.password}@{self._config.host}:{self._config.port}/{self._config.database_name}",
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
            logger.error(f"Command failed. Return code : {process.returncode}")
            logger.error("Error output:", error.decode("utf-8"))
            return

        for line in output.splitlines():
            print(line.decode("utf-8"))
