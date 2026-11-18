from datetime import datetime
from pathlib import Path
from sqlite3 import Connection

from sqlalchemy import URL, DateTime, ForeignKey, String, create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))


class UserSession(Base):
    __tablename__ = "sessions"

    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(), index=True)


def database_url(path: Path) -> URL:
    return URL.create("sqlite", database=str(path))


def create_database_engine(path: Path) -> Engine:
    engine = create_engine(database_url(path), hide_parameters=True)

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection: Connection, _record: object) -> None:
        cursor = connection.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine
