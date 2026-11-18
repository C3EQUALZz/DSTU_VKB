from datetime import UTC, datetime, timedelta
from hashlib import sha256
from secrets import token_urlsafe

from sqlalchemy import delete, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from blast_furnace.application.identity import AccountAlreadyExists, CurrentUser
from blast_furnace.infrastructure.database import User, UserSession

SESSION_LIFETIME = timedelta(hours=1)
PBKDF2_METHOD = "pbkdf2:sha256:1000000"
DUMMY_HASH = generate_password_hash(token_urlsafe(), method=PBKDF2_METHOD)


class DatabaseIdentityStore:
    def __init__(self, sessions: sessionmaker[Session]) -> None:
        self._sessions = sessions

    def register(
        self, username: str, email: str, password: str, previous_session_id: str | None
    ) -> str:
        password_hash = generate_password_hash(password, method=PBKDF2_METHOD)
        try:
            with self._sessions.begin() as db:
                user = User(username=username, email=email, password_hash=password_hash)
                db.add(user)
                db.flush()
                return self._rotate_session(db, user.id, previous_session_id)
        except IntegrityError:
            with self._sessions() as db:
                exists = db.scalar(
                    select(User.id).where(
                        or_(User.username == username, User.email == email)
                    )
                )
            if exists is not None:
                raise AccountAlreadyExists from None
            raise

    def login(
        self, username: str, password: str, previous_session_id: str | None
    ) -> str | None:
        with self._sessions.begin() as db:
            user = db.scalar(select(User).where(User.username == username))
            password_hash = user.password_hash if user is not None else DUMMY_HASH
            valid_password = check_password_hash(password_hash, password)
            if user is None or not valid_password:
                return None
            return self._rotate_session(db, user.id, previous_session_id)

    def resolve(self, session_id: str | None) -> CurrentUser | None:
        cutoff = _utc_now() - SESSION_LIFETIME
        with self._sessions.begin() as db:
            expired = UserSession.created_at <= cutoff
            if db.scalar(select(UserSession.session_id).where(expired).limit(1)):
                db.execute(delete(UserSession).where(expired))
            if session_id is None:
                return None
            user = db.scalar(
                select(User)
                .join(UserSession)
                .where(
                    UserSession.session_id == _session_digest(session_id),
                    UserSession.created_at > cutoff,
                )
            )
            return CurrentUser(user.id, user.username) if user is not None else None

    def revoke(self, session_id: str) -> None:
        with self._sessions.begin() as db:
            self._delete_session(db, session_id)

    @staticmethod
    def _delete_session(db: Session, session_id: str) -> None:
        db.execute(
            delete(UserSession).where(
                UserSession.session_id == _session_digest(session_id)
            )
        )

    def _rotate_session(
        self, db: Session, user_id: int, previous_session_id: str | None
    ) -> str:
        if previous_session_id is not None:
            self._delete_session(db, previous_session_id)
        session_id = token_urlsafe(32)
        db.add(
            UserSession(
                session_id=_session_digest(session_id),
                user_id=user_id,
                created_at=_utc_now(),
            )
        )
        return session_id


def _session_digest(session_id: str) -> str:
    return sha256(session_id.encode()).hexdigest()


def _utc_now() -> datetime:
    # SQLite stores dates without a timezone. Every timestamp here represents UTC.
    return datetime.now(UTC).replace(tzinfo=None)
