from collections.abc import Iterator
from dataclasses import replace
from datetime import datetime, timedelta
from hashlib import sha256

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from blast_furnace.infrastructure import identity
from blast_furnace.infrastructure.database import (
    User,
    UserSession,
    create_database_engine,
)
from blast_furnace.setup.app_factory import create_app
from blast_furnace.setup.config import Settings
from tests.forms import EMAIL, PASSWORD, USERNAME, post_form, register


@pytest.fixture
def database(settings: Settings) -> Iterator[Session]:
    engine = create_database_engine(settings.database_path)
    try:
        with Session(engine) as db:
            yield db
    finally:
        engine.dispose()


@pytest.mark.parametrize("path", ["/tempr", "/compare"])
@pytest.mark.parametrize("method", ["GET", "POST"])
def test_calculations_require_login(client: FlaskClient, path: str, method: str) -> None:
    response = client.open(path, method=method)
    assert response.status_code == 302
    assert response.location == "/login"


def test_login_form_has_public_styles(client: FlaskClient) -> None:
    assert client.get("/login").status_code == 200
    assert client.get("/static/styles.css").mimetype == "text/css"


def test_registration_saves_email_hash_and_persistent_session(
    client: FlaskClient, database: Session
) -> None:
    response = register(client, username=f"  {USERNAME}  ", email="anna@EXAMPLE.org")
    assert response.status_code == 303
    assert response.location == "/"
    cookie_header = response.headers["Set-Cookie"]
    assert "HttpOnly" in cookie_header
    assert "SameSite=Lax" in cookie_header
    assert "Secure;" not in cookie_header
    assert "Expires=" in cookie_header

    user = database.scalars(select(User)).one()
    assert user.username == USERNAME
    assert user.email == EMAIL
    assert user.password_hash.startswith("pbkdf2:sha256:")
    assert check_password_hash(user.password_hash, PASSWORD)
    assert not check_password_hash(user.password_hash, PASSWORD.strip())
    record = database.scalars(select(UserSession)).one()
    assert record.user_id == user.id

    with client.session_transaction() as data:
        assert set(data) == {"session_id", "_permanent"}
        assert record.session_id == sha256(data["session_id"].encode()).hexdigest()
    assert 'class="username">anna<' in client.get("/").text
    assert client.get("/tempr").status_code == 200
    assert client.get("/compare").status_code == 200


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("email", "invalid", "Введите действительный адрес электронной почты."),
        ("username", "", "Введите имя пользователя"),
        ("password", "short", "Пароль должен содержать"),
        ("password_confirm", "different password", "Пароли не совпадают."),
    ],
)
def test_registration_checks_fields(
    client: FlaskClient, database: Session, field: str, value: str, message: str
) -> None:
    response = register(client, **{field: value})
    assert response.status_code == 400
    assert message in response.text
    assert database.scalar(select(User.id)) is None


def test_duplicate_accounts_are_rejected(app: Flask, signed_in: FlaskClient) -> None:
    guest = app.test_client()
    assert register(guest, email="other@example.org").status_code == 409
    assert register(guest, username="other").status_code == 409
    assert guest.get("/tempr").status_code == 302
    assert signed_in.get("/tempr").status_code == 200


def test_bad_login_has_same_message_for_wrong_password_and_unknown_user(
    app: Flask, signed_in: FlaskClient
) -> None:
    guest = app.test_client()
    assert signed_in.get("/tempr").status_code == 200
    for username in (USERNAME, "unknown"):
        response = post_form(
            guest, "/login", {"username": username, "password": "Неверный пароль"}
        )
        assert response.status_code == 401
        assert "Неверное имя или пароль." in response.text
    assert guest.get("/compare").status_code == 302


def test_login_rotates_current_session(signed_in: FlaskClient, database: Session) -> None:
    previous = database.scalars(select(UserSession.session_id)).one()
    response = post_form(
        signed_in, "/login", {"username": USERNAME, "password": PASSWORD}
    )
    assert response.status_code == 303
    assert database.scalars(select(UserSession.session_id)).one() != previous


def test_logout_revokes_current_session_only(
    app: Flask, signed_in: FlaskClient, database: Session
) -> None:
    second_browser = app.test_client()
    login = post_form(
        second_browser, "/login", {"username": USERNAME, "password": PASSWORD}
    )
    assert login.status_code == 303
    first_cookie = signed_in.get_cookie("session")
    assert first_cookie is not None
    assert signed_in.get("/logout").status_code == 405
    response = post_form(signed_in, "/logout", {}, form_page="/")
    assert response.status_code == 303
    assert response.location == "/"
    assert signed_in.get_cookie("session") is None
    assert len(database.scalars(select(UserSession.session_id)).all()) == 1
    assert second_browser.get("/tempr").status_code == 200

    signed_in.set_cookie("session", first_cookie.value)
    assert signed_in.get("/compare").location == "/login"


def test_every_post_form_requires_a_csrf_token(client: FlaskClient) -> None:
    assert client.post("/register").status_code == 400
    assert client.post("/login").status_code == 400
    assert register(client).status_code == 303
    for path in ("/tempr", "/compare", "/logout"):
        assert client.post(path, data={"csrf_token": "неверный токен"}).status_code == 400
    assert client.get("/tempr").status_code == 200


def test_wrong_cookie_signature_is_rejected(signed_in: FlaskClient) -> None:
    cookie = signed_in.get_cookie("session")
    assert cookie is not None
    prefix, signature = cookie.value.rsplit(".", 1)
    replacement = "A" if signature[0] != "A" else "B"
    signed_in.set_cookie("session", f"{prefix}.{replacement}{signature[1:]}")
    assert signed_in.get("/compare").location == "/login"


def test_active_session_survives_application_restart(
    signed_in: FlaskClient, settings: Settings
) -> None:
    cookie = signed_in.get_cookie("session")
    assert cookie is not None
    restarted = create_app(settings).test_client()
    restarted.set_cookie("session", cookie.value)
    assert restarted.get("/compare").status_code == 200


def test_cookie_secure_flag_is_enabled_for_https(settings: Settings) -> None:
    app = create_app(replace(settings, secure_cookies=True))
    response = app.test_client().get("/login", base_url="https://localhost")
    assert "Secure" in response.headers["Set-Cookie"]


def test_middleware_removes_sessions_at_one_hour(
    app: Flask, client: FlaskClient, database: Session, monkeypatch: pytest.MonkeyPatch
) -> None:
    started = datetime(2026, 11, 18, 12)
    monkeypatch.setattr(identity, "_utc_now", lambda: started)
    assert register(client).status_code == 303

    monkeypatch.setattr(identity, "_utc_now", lambda: started + timedelta(minutes=59))
    assert client.get("/tempr").status_code == 200
    second_browser = app.test_client()
    login = post_form(
        second_browser, "/login", {"username": USERNAME, "password": PASSWORD}
    )
    assert login.status_code == 303

    monkeypatch.setattr(identity, "_utc_now", lambda: started + timedelta(hours=1))
    # A public page request triggers cleanup even when it has no cookie.
    assert app.test_client().get("/").status_code == 200
    remaining = database.scalars(select(UserSession.created_at)).one()
    assert remaining == started + timedelta(minutes=59)
    assert client.get("/tempr").location == "/login"
    assert second_browser.get("/tempr").status_code == 200
