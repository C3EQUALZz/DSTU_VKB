"""Тесты построителя плана встраивания."""

import pytest

from steganography.domain.common.encodings.fixed_width_encoding import (
    FixedWidthEncoding,
)
from steganography.domain.common.value_objects.formatting_method import (
    FormattingMethod,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from steganography.domain.text_format_encode.errors.encode_errors import (
    ContainerTooSmallError,
    UnencodableSecretError,
)
from steganography.domain.text_format_encode.services.container_plan_builder import (
    ContainerPlanBuilder,
)
from steganography.domain.text_format_encode.value_objects.cover_text import (
    CoverText,
)
from steganography.domain.text_format_encode.value_objects.secret_payload import (
    SecretPayload,
)

_WIN1251 = FixedWidthEncoding(name="Windows-1251", codec="windows-1251")
_METHOD = FormattingMethod(
    param=FormattingParam.SIZE, zero_value="28", one_value="29",
)


@pytest.fixture
def builder() -> ContainerPlanBuilder:
    return ContainerPlanBuilder()


def test_plan_marks_one_bits_with_one_value(
    builder: ContainerPlanBuilder,
) -> None:
    payload = SecretPayload(
        secret_text="A", encoding=_WIN1251, method=_METHOD,
    )
    cover = CoverText.from_plain("a" * 64)
    plan = builder.build(payload, cover)

    # "A" = 0x41 = 01000001 → единицы на позициях 1 и 7
    bits = "".join("1" if cf.is_one else "0" for cf in plan.chars[:8])
    assert bits == "01000001"
    assert plan.chars[1].value == "29"
    assert plan.chars[0].value == "28"
    assert plan.payload_bits == 8


def test_tail_after_message_uses_zero_value(
    builder: ContainerPlanBuilder,
) -> None:
    payload = SecretPayload(
        secret_text="A", encoding=_WIN1251, method=_METHOD,
    )
    plan = builder.build(payload, CoverText.from_plain("a" * 20))
    assert all(not cf.is_one for cf in plan.chars[8:])


def test_raises_when_container_too_small(
    builder: ContainerPlanBuilder,
) -> None:
    payload = SecretPayload(
        secret_text="длинное сообщение", encoding=_WIN1251, method=_METHOD,
    )
    with pytest.raises(ContainerTooSmallError):
        builder.build(payload, CoverText.from_plain("коротко"))


def test_raises_when_secret_unencodable(
    builder: ContainerPlanBuilder,
) -> None:
    koi8r = FixedWidthEncoding(name="КОИ-8R", codec="koi8-r")
    payload = SecretPayload(
        secret_text="ひらがな", encoding=koi8r, method=_METHOD,
    )
    with pytest.raises(UnencodableSecretError):
        builder.build(payload, CoverText.from_plain("a" * 100))
