from pathlib import Path

from alembic import context

from blast_furnace.infrastructure.database import (
    Base,
    create_database_engine,
    database_url,
)
from blast_furnace.setup.config import database_path_from_env

config = context.config
path: Path = config.attributes.get("database_path") or database_path_from_env()

if context.is_offline_mode():
    context.configure(
        url=database_url(path), target_metadata=Base.metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_database_engine(path)
    try:
        with engine.connect() as connection:
            context.configure(
                connection=connection, target_metadata=Base.metadata, render_as_batch=True
            )
            with context.begin_transaction():
                context.run_migrations()
    finally:
        engine.dispose()
