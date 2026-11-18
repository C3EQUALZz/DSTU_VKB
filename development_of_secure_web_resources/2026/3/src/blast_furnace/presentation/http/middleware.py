from secrets import compare_digest, token_urlsafe

from dishka import Container
from flask import (
    Flask,
    Response,
    abort,
    current_app,
    g,
    redirect,
    request,
    session,
    url_for,
)
from flask.typing import ResponseReturnValue
from itsdangerous import Signer

from blast_furnace.application.identity import IdentityStore

PUBLIC_ENDPOINTS = {"pages.index", "auth.login", "auth.register", "pages.static"}


def browser_session_id() -> str | None:
    value = session.get("session_id")
    return value if isinstance(value, str) else None


def csrf_token() -> str:
    seed = browser_session_id() or session.get("csrf_seed")
    if seed is None:
        seed = session["csrf_seed"] = token_urlsafe(32)
    return _csrf_signer().get_signature(seed).decode("ascii")


def _csrf_signer() -> Signer:
    return Signer(current_app.config["SECRET_KEY"], salt="securedev.form-csrf")


def install_auth_middleware(app: Flask) -> None:
    app.add_template_global(csrf_token)

    @app.before_request
    def authorize() -> ResponseReturnValue | None:
        # Let Flask handle routing errors and serve CSS without consulting the database.
        if request.endpoint is None or request.endpoint == "pages.static":
            return None

        container: Container = g.dishka_container
        store = container.get(IdentityStore)
        session_id = browser_session_id()
        g.current_user = store.resolve(session_id)
        if session_id is not None and g.current_user is None:
            session.clear()
        if request.endpoint not in PUBLIC_ENDPOINTS and g.current_user is None:
            return redirect(url_for("auth.login"))

        if request.method == "POST":
            seed = browser_session_id() or session.get("csrf_seed")
            submitted = request.form.get("csrf_token", "").encode()
            if seed is None or not compare_digest(
                _csrf_signer().get_signature(seed), submitted
            ):
                abort(
                    400,
                    description="Форма устарела. Откройте страницу и попробуйте снова.",
                )
        return None

    @app.after_request
    def prevent_caching(response: Response) -> Response:
        if request.endpoint is not None and request.endpoint != "pages.static":
            response.cache_control.no_store = True
        return response
