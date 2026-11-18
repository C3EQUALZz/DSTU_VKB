import atexit

from dishka import make_container
from dishka.integrations.flask import setup_dishka
from flask import Flask, current_app
from sqlalchemy.exc import SQLAlchemyError

from blast_furnace.infrastructure.identity import SESSION_LIFETIME
from blast_furnace.presentation.http.auth import auth
from blast_furnace.presentation.http.middleware import install_auth_middleware
from blast_furnace.presentation.http.routes import pages
from blast_furnace.setup.config import Settings
from blast_furnace.setup.ioc import ApplicationProvider


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings.from_env()
    app = Flask("blast_furnace", static_folder=None)
    app.config.from_mapping(
        AUTHOR_NAME=settings.author_name,
        COPYRIGHT_YEAR=settings.copyright_year,
        MAX_CONTENT_LENGTH=16 * 1024,
        SECRET_KEY=settings.secret_key,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=settings.secure_cookies,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_REFRESH_EACH_REQUEST=False,
        PERMANENT_SESSION_LIFETIME=SESSION_LIFETIME,
    )
    app.register_blueprint(pages)
    app.register_blueprint(auth)
    container = make_container(
        ApplicationProvider(),
        context={Settings: settings},
    )
    setup_dishka(container=container, app=app)
    install_auth_middleware(app)

    @app.errorhandler(SQLAlchemyError)
    def database_error(error: SQLAlchemyError) -> tuple[str, int]:
        current_app.logger.error("Ошибка базы данных", exc_info=error)
        return "База данных временно недоступна.", 503

    atexit.register(container.close)
    return app
