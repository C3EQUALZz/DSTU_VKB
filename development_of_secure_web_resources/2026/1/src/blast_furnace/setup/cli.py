from flask.cli import FlaskGroup

from blast_furnace.setup.app_factory import create_app


def main() -> None:
    FlaskGroup(create_app=create_app)()
