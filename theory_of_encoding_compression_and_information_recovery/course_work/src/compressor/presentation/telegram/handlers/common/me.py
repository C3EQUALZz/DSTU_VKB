from collections import deque
from collections.abc import Mapping
from typing import Final

from aiogram import Router
from aiogram.enums import ChatType, ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from compressor.application.common.views.users import UserView
from compressor.application.queries.user.read_current_user import (
    ReadCurrentTelegramUserQuery,
    ReadCurrentTelegramUserQueryHandler,
)
from compressor.presentation.telegram.filters.chat import ChatTypeFilter
from compressor.presentation.telegram.handlers.common.consts import (
    ADMIN,
    LANGUAGE,
    ME,
    NAME,
    SUPER_ADMIN,
    SUPPORT,
    TELEGRAM_ACCOUNT_ID,
    TELEGRAM_ACCOUNT_TITLE,
    USER,
    USER_INFO_TITLE,
)

router: Final[Router] = Router()


def format_view(view: UserView, i18n: I18nContext) -> str:
    row_roles_and_i18n_values_mapping: Mapping[str, str] = {
        "admin": ADMIN,
        "user": USER,
        "support": SUPPORT,
        "super_admin": SUPER_ADMIN
    }

    lines: deque[str] = deque()

    lines.append(i18n.get(USER_INFO_TITLE))
    lines.append(f"{i18n.get(NAME)} {view.first_name}")
    lines.append(i18n.get(row_roles_and_i18n_values_mapping.get(view.role)))
    lines.append(i18n.get(LANGUAGE))

    if view.telegram_id:
        lines.append("")
        lines.append(i18n.get(TELEGRAM_ACCOUNT_TITLE))
        lines.append(
            i18n.get(
                TELEGRAM_ACCOUNT_ID,
                telegram_id=view.telegram_id
            )
        )

    return "\n".join(lines)


@router.message(
    ChatTypeFilter(allowed_chat_types=[ChatType.PRIVATE]),
    Command(commands=[ME])
)
async def cmd_me_handler(
        message: Message,
        interactor: FromDishka[ReadCurrentTelegramUserQueryHandler],
        i18n: I18nContext
) -> None:
    query: ReadCurrentTelegramUserQuery = ReadCurrentTelegramUserQuery()
    view: UserView = await interactor(query)
    await message.reply(
        text=format_view(view, i18n=i18n),
        parse_mode=ParseMode.HTML
    )
