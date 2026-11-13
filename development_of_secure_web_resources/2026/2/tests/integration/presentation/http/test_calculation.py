from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from flask.testing import FlaskClient

from blast_furnace.setup.app_factory import create_app
from blast_furnace.setup.config import Settings

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
    client: FlaskClient, tmp_path: Path, numbers: tuple[str, ...], expected: str
) -> None:
    data = dict(zip(BASE_FORM, numbers, strict=True))
    data["comment"] = "Контрольный расчёт"
    response = client.post("/tempr", data=data)
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
    client: FlaskClient, tmp_path: Path, field: str, value: str
) -> None:
    response = client.post("/tempr", data=BASE_FORM | {field: value})
    assert response.status_code == 400
    assert 'role="alert"' in response.text
    assert 'id="temperature-result"' not in response.text
    assert not (tmp_path / "calc_log.txt").exists()


def test_missing_fields_are_handled(client: FlaskClient, tmp_path: Path) -> None:
    assert client.post("/tempr", data={}).status_code == 400
    assert not (tmp_path / "calc_log.txt").exists()


def test_comment_is_optional_and_records_are_appended(
    client: FlaskClient, tmp_path: Path
) -> None:
    client.post("/tempr", data=BASE_FORM)
    client.post("/tempr", data=BASE_FORM | {"comment": "Второй расчёт"})
    lines = (tmp_path / "calc_log.txt").read_text().splitlines()
    assert len(lines) == 2
    assert lines[1].endswith("Второй расчёт")


def test_comment_is_escaped_in_html_and_log(client: FlaskClient, tmp_path: Path) -> None:
    comment = '<script>alert("x")</script>\r\nПоддельная запись |'
    response = client.post("/tempr", data=BASE_FORM | {"comment": comment})
    assert response.status_code == 200
    assert "<script>" not in response.text
    assert "&lt;script&gt;" in response.text
    log = (tmp_path / "calc_log.txt").read_text()
    assert len(log.splitlines()) == 1
    assert "\\r\\nПоддельная запись \\|" in log


def test_unwritable_log_returns_service_unavailable(tmp_path: Path) -> None:
    # Каталог вместо файла воспроизводимо вызывает ошибку записи даже от root.
    app = create_app(Settings(log_path=tmp_path))
    response = app.test_client().post("/tempr", data=BASE_FORM)
    assert response.status_code == 503
    assert "Не удалось сохранить расчёт" in response.text
    assert 'id="temperature-result"' not in response.text


def test_log_directory_is_created(tmp_path: Path) -> None:
    log_path = tmp_path / "nested" / "calc_log.txt"
    app = create_app(Settings(log_path=log_path))
    response = app.test_client().post("/tempr", data=BASE_FORM)
    assert response.status_code == 200
    assert log_path.is_file()


def test_large_request_is_rejected(client: FlaskClient) -> None:
    assert (
        client.post("/tempr", data=BASE_FORM | {"comment": "x" * 17000}).status_code
        == 413
    )
