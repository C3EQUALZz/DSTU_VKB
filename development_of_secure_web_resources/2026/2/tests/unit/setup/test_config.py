import pytest

from blast_furnace.setup.config import Settings


def test_author_can_be_overridden_without_editing_templates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AUTHOR_NAME", "Другой автор")

    settings = Settings.from_env()

    assert settings.author_name == "Другой автор"
