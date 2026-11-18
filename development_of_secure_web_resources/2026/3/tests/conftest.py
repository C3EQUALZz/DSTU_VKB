from collections.abc import Iterator
from pathlib import Path
from secrets import token_hex

import pytest
from alembic import command
from alembic.config import Config
from flask import Flask
from flask.testing import FlaskClient

from blast_furnace.setup.app_factory import create_app
from blast_furnace.setup.config import Settings
from tests.forms import register


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    result = Settings(
        secret_key=token_hex(32),
        database_path=tmp_path / "securedev.db",
        log_path=tmp_path / "calc_log.txt",
    )
    config = Config(Path(__file__).resolve().parents[1] / "alembic.ini")
    config.attributes["database_path"] = result.database_path
    command.upgrade(config, "head")
    return result


@pytest.fixture
def app(settings: Settings) -> Flask:
    app = create_app(settings)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app: Flask) -> Iterator[FlaskClient]:
    with app.test_client() as client:
        yield client


@pytest.fixture
def signed_in(client: FlaskClient) -> FlaskClient:
    assert register(client).status_code == 303
    return client
