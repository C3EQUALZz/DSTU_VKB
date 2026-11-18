from bs4 import BeautifulSoup
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

USERNAME = "anna"
EMAIL = "anna@example.org"
PASSWORD = "  Учебный пароль 2026  "


def post_form(
    client: FlaskClient,
    path: str,
    data: dict[str, str],
    *,
    form_page: str | None = None,
) -> TestResponse:
    page = BeautifulSoup(client.get(form_page or path).text, "html.parser")
    token = page.select_one(f'form[action="{path}"] input[name="csrf_token"]')
    assert token is not None
    return client.post(path, data=data | {"csrf_token": str(token["value"])})


def register(client: FlaskClient, **overrides: str) -> TestResponse:
    fields = {
        "username": USERNAME,
        "email": EMAIL,
        "password": PASSWORD,
        "password_confirm": PASSWORD,
    }
    return post_form(client, "/register", fields | overrides)
