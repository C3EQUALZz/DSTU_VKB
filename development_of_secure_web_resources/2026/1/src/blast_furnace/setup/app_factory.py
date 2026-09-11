import atexit

from dishka import make_container
from dishka.integrations.flask import setup_dishka
from flask import Flask

from blast_furnace.presentation.http.routes import pages
from blast_furnace.setup.config import Settings
from blast_furnace.setup.ioc import ApplicationProvider


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings.from_env()
    app = Flask("blast_furnace", static_folder=None)
    app.config.from_mapping(
        AUTHOR_NAME=settings.author_name,
        COPYRIGHT_YEAR=settings.copyright_year,
    )
    app.register_blueprint(pages)
    container = make_container(ApplicationProvider())
    setup_dishka(container=container, app=app)
    atexit.register(container.close)
    return app
