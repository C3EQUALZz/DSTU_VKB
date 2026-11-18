from secrets import token_hex

import pytest

from blast_furnace.setup.config import Settings


def test_author_can_be_overridden_without_editing_templates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AUTHOR_NAME", "Другой автор")
    monkeypatch.setenv("SECRET_KEY", token_hex(32))

    settings = Settings.from_env()

    assert settings.author_name == "Другой автор"


def test_secret_key_is_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SECRET_KEY", raising=False)
    with pytest.raises(ValueError, match="SECRET_KEY"):
        Settings.from_env()
