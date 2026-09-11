import pytest
from bs4 import BeautifulSoup
from flask import Flask
from flask.testing import FlaskClient

from blast_furnace.setup.app_factory import create_app
from blast_furnace.setup.config import Settings


def test_homepage_matches_the_assignment(client: FlaskClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.mimetype == "text/html"
    page = BeautifulSoup(response.text, "html.parser")
    assert page.select_one('html[lang="ru"]') is not None
    assert page.select_one('meta[charset="UTF-8"]') is not None
    assert page.select_one("header h1") is not None
    assert page.select_one('header nav a[href="/tempr"]') is not None
    assert page.select_one("main table") is not None
    footer = page.select_one("footer")
    assert footer is not None
    assert "Ковалев Данил Петрович" in footer.get_text()
    rows = [
        [cell.get_text(strip=True) for cell in row.select("th, td")]
        for row in page.select("main table tbody tr")
    ]
    assert rows == [
        ["1", "Температура дутья", "100", "0,5", "1,0"],
        ["2", "Горячая прочность кокса", "1", "1", "1,6"],
        ["3", "Расход природного газа", "10", "0,5", "1,0"],
    ]


def test_temperature_page_explains_next_part(client: FlaskClient) -> None:
    response = client.get("/tempr")

    assert response.status_code == 200
    assert "во второй части работы" in response.text
    assert "<form" not in response.text


def test_all_local_links_and_styles_are_available(client: FlaskClient) -> None:
    for path in ("/", "/tempr"):
        page = BeautifulSoup(client.get(path).text, "html.parser")
        for link in page.select("a[href], link[href]"):
            href = str(link["href"])
            if href.startswith("/"):
                assert client.get(href).status_code == 200


@pytest.mark.parametrize("path", ["/", "/tempr"])
@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE"])
def test_read_only_pages_reject_writes(
    client: FlaskClient,
    path: str,
    method: str,
) -> None:
    response = client.open(path, method=method)

    assert response.status_code == 405


def test_unknown_page_returns_not_found(client: FlaskClient) -> None:
    assert client.get("/missing").status_code == 404


def test_author_is_escaped_and_settings_do_not_leak(app: Flask) -> None:
    other = create_app(Settings(author_name='<script>alert("x")</script>'))

    response = other.test_client().get("/")

    assert "<script>" not in response.text
    assert "&lt;script&gt;" in response.text
    assert app.config["AUTHOR_NAME"] == "Ковалев Данил Петрович"


def test_debug_is_disabled_by_default(app: Flask) -> None:
    assert app.debug is False
