from collections.abc import Iterator
from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient

from blast_furnace.setup.app_factory import create_app
from blast_furnace.setup.config import Settings


@pytest.fixture
def app(tmp_path: Path) -> Flask:
    app = create_app(
        Settings(author_name="Ковалев Данил Петрович", log_path=tmp_path / "calc_log.txt")
    )
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app: Flask) -> Iterator[FlaskClient]:
    with app.test_client() as client:
        yield client
