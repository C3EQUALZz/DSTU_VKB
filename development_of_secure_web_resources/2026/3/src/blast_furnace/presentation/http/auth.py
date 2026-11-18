from dishka.integrations.flask import FromDishka, inject
from email_validator import EmailNotValidError, validate_email
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.wrappers import Response

from blast_furnace.application.identity import AccountAlreadyExists, IdentityStore
from blast_furnace.presentation.http.middleware import browser_session_id

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
@inject
def register(store: FromDishka[IdentityStore]) -> Response | tuple[str, int]:
    if request.method == "GET":
        return _form(registering=True)
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    if not 1 <= len(username) <= 50 or not username.isprintable():
        error = "Введите имя пользователя длиной до 50 символов."
    elif not 12 <= len(password) <= 128:
        error = "Пароль должен содержать от 12 до 128 символов."
    elif password != request.form.get("password_confirm"):
        error = "Пароли не совпадают."
    else:
        try:
            email = validate_email(email, check_deliverability=False).normalized
        except EmailNotValidError:
            error = "Введите действительный адрес электронной почты."
        else:
            try:
                session_id = store.register(
                    username, email, password, browser_session_id()
                )
            except AccountAlreadyExists:
                return _form(
                    registering=True,
                    username=username,
                    email=email,
                    error="Имя пользователя или email уже используется.",
                    status=409,
                )
            return _start_session(session_id)
    return _form(
        registering=True, username=username, email=email, error=error, status=400
    )


@auth.route("/login", methods=["GET", "POST"])
@inject
def login(store: FromDishka[IdentityStore]) -> Response | tuple[str, int]:
    if request.method == "GET":
        return _form(registering=False)
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if len(password) <= 128:
        session_id = store.login(username, password, browser_session_id())
        if session_id is not None:
            return _start_session(session_id)
    return _form(
        registering=False, username=username, error="Неверное имя или пароль.", status=401
    )


@auth.post("/logout")
@inject
def logout(store: FromDishka[IdentityStore]) -> Response:
    store.revoke(session["session_id"])
    session.clear()
    return redirect(url_for("pages.index"), code=303)


def _start_session(session_id: str) -> Response:
    session.clear()
    session["session_id"] = session_id
    session.permanent = True
    return redirect(url_for("pages.index"), code=303)


def _form(
    *,
    registering: bool,
    username: str = "",
    email: str = "",
    error: str | None = None,
    status: int = 200,
) -> tuple[str, int]:
    return render_template(
        "auth_form.html",
        registering=registering,
        username=username,
        email=email,
        error=error,
    ), status
