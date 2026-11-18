from dataclasses import replace
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from flask.testing import FlaskClient

from blast_furnace.setup.app_factory import create_app
from blast_furnace.setup.config import Settings
from tests.forms import post_form, register

BASE_FORM = {"t_blast": "1000", "humidity": "10", "oxygen": "21", "gas": "0"}


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        (("1000", "10", "21", "0"), "2201,0"),
        (("1200", "15", "25", "8"), "2080,0"),
        (("1100", "20", "23", "5"), "2048,0"),
        (("1300", "1", "35", "0"), "3076,6"),
        (("1000,5", "10.5", "21", "0"), "2198,7"),
        (("900", "40", "21", "15"), "1184,0"),
    ],
)
def test_post_calculates_and_logs(
    signed_in: FlaskClient, tmp_path: Path, numbers: tuple[str, ...], expected: str
) -> None:
    data = dict(zip(BASE_FORM, numbers, strict=True))
    data["comment"] = "Контрольный расчёт"
    response = post_form(signed_in, "/tempr", data)
    assert response.status_code == 200
    page = BeautifulSoup(response.text, "html.parser")
    output = page.select_one("#temperature-result")
    assert output is not None and output.text == expected
    assert page.select_one('input[name="t_blast"][value="' + numbers[0] + '"]')
    log = (tmp_path / "calc_log.txt").read_text()
    assert f"Тг={expected.replace(',', '.')} | Контрольный расчёт" in log
    assert len(log.splitlines()) == 1


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("t_blast", ""),
        ("humidity", "abc"),
        ("t_blast", "899"),
        ("t_blast", "1301"),
        ("humidity", "0"),
        ("humidity", "41"),
        ("oxygen", "20"),
        ("oxygen", "36"),
        ("gas", "-1"),
        ("gas", "16"),
        ("oxygen", "NaN"),
        ("gas", "inf"),
        ("t_blast", "1e999"),
        ("comment", "x" * 501),
    ],
)
def test_invalid_input_does_not_log(
    signed_in: FlaskClient, tmp_path: Path, field: str, value: str
) -> None:
    response = post_form(signed_in, "/tempr", BASE_FORM | {field: value})
    assert response.status_code == 400
    assert 'role="alert"' in response.text
    assert 'id="temperature-result"' not in response.text
    assert not (tmp_path / "calc_log.txt").exists()


def test_missing_fields_are_handled(signed_in: FlaskClient, tmp_path: Path) -> None:
    assert post_form(signed_in, "/tempr", {}).status_code == 400
    assert not (tmp_path / "calc_log.txt").exists()


def test_comment_is_optional_and_records_are_appended(
    signed_in: FlaskClient, tmp_path: Path
) -> None:
    post_form(signed_in, "/tempr", BASE_FORM)
    post_form(signed_in, "/tempr", BASE_FORM | {"comment": "Второй расчёт"})
    lines = (tmp_path / "calc_log.txt").read_text().splitlines()
    assert len(lines) == 2
    assert lines[1].endswith("Второй расчёт")


def test_comment_is_escaped_in_html_and_log(
    signed_in: FlaskClient, tmp_path: Path
) -> None:
    comment = '<script>alert("x")</script>\r\nПоддельная запись |'
    response = post_form(signed_in, "/tempr", BASE_FORM | {"comment": comment})
    assert response.status_code == 200
    assert "<script>" not in response.text
    assert "&lt;script&gt;" in response.text
    log = (tmp_path / "calc_log.txt").read_text()
    assert len(log.splitlines()) == 1
    assert "\\r\\nПоддельная запись \\|" in log


def test_unwritable_log_returns_service_unavailable(
    tmp_path: Path, settings: Settings
) -> None:
    # Каталог вместо файла воспроизводимо вызывает ошибку записи даже от root.
    app = create_app(replace(settings, log_path=tmp_path))
    client = app.test_client()
    assert register(client).status_code == 303
    response = post_form(client, "/tempr", BASE_FORM)
    assert response.status_code == 503
    assert "Не удалось сохранить расчёт" in response.text
    assert 'id="temperature-result"' not in response.text


def test_log_directory_is_created(tmp_path: Path, settings: Settings) -> None:
    log_path = tmp_path / "nested" / "calc_log.txt"
    app = create_app(replace(settings, log_path=log_path))
    client = app.test_client()
    assert register(client).status_code == 303
    response = post_form(client, "/tempr", BASE_FORM)
    assert response.status_code == 200
    assert log_path.is_file()


def test_large_request_is_rejected(signed_in: FlaskClient) -> None:
    assert (
        post_form(signed_in, "/tempr", BASE_FORM | {"comment": "x" * 17000}).status_code
        == 413
    )
