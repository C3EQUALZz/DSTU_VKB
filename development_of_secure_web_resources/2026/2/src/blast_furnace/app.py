"""WSGI entry point: gunicorn blast_furnace.app:app."""

from blast_furnace.setup.app_factory import create_app
from blast_furnace.setup.cli import main

app = create_app()

if __name__ == "__main__":
    main()
