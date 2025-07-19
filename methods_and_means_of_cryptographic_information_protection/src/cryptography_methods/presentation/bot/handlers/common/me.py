from typing import Final, Mapping

from aiogram import Router
from aiogram.enums import ParseMode, ChatType
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from cryptography_methods.application.common.views.user import UserView
from cryptography_methods.application.queries.user.read_current_user import (
    ReadCurrentUserQueryHandler,
    ReadCurrentUserQuery
)
from cryptography_methods.presentation.bot.filters.chat import ChatTypeFilter

from cryptography_methods.presentation.bot.handlers.common.consts import (
    ME,
    USER_INFO_TITLE,
    NAME,
    SECOND_NAME,
    ADMIN,
    USER,
    SUPPORT,
    SUPER_ADMIN,
    TELEGRAM_ACCOUNT_TITLE,
    TELEGRAM_ACCOUNT_ID,
    LANGUAGE
)

router: Final[Router] = Router()


def format_view(view: UserView, i18n: I18nContext) -> str:
    row_roles_and_i18n_values_mapping: Mapping[str, str] = {
        "admin": ADMIN,
        "user": USER,
        "support": SUPPORT,
        "super_admin": SUPER_ADMIN
    }

    lines: list[str] = [
        i18n.get(USER_INFO_TITLE),
        "",
        f"{i18n.get(NAME)} {view.first_name}"
    ]

    if view.last_name:
        lines.append(f"{i18n.get(SECOND_NAME)} {view.last_name}")

    lines.append(
        i18n.get(
            row_roles_and_i18n_values_mapping.get(
                view.role
            ),
        )
    )

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
        interactor: FromDishka[ReadCurrentUserQueryHandler],
        i18n: I18nContext
) -> None:
    query: ReadCurrentUserQuery = ReadCurrentUserQuery()
    view: UserView = await interactor(query)
    await message.reply(
        text=format_view(view, i18n=i18n),
        parse_mode=ParseMode.HTML
    )
