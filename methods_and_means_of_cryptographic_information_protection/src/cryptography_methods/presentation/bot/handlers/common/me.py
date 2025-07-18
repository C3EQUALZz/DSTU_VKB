from typing import Final, Mapping

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from dishka import FromDishka

from cryptography_methods.application.common.views.user import UserView
from cryptography_methods.application.queries.user.read_current_user import (
    ReadCurrentUserQueryHandler,
    ReadCurrentUserQuery
)
from cryptography_methods.presentation.bot.handlers.common.consts import ME

router: Final[Router] = Router()


def format_view(view: UserView) -> str:
    emojis_and_roles: Mapping[str, str] = {
        "admin": "👑",
        "user": "👤",
        "support": "🛡️",
        "super_admin": "💎"
    }

    role_emoji: str = emojis_and_roles.get(view.role.lower(), "👤")

    lines: list[str] = [
        f"{role_emoji} <b>Информация о пользователе</b>",
        f"",
        f"<b>Имя:</b> {view.first_name}"
    ]

    if view.last_name:
        lines.append(f"<b>Фамилия:</b> {view.last_name}")

    lines.append(f"<b>Роль:</b> {view.role.capitalize()} {role_emoji}")

    if view.telegram_id:
        lines.append("")
        lines.append(f"🔗 <b>Telegram аккаунт</b>")
        lines.append(f"🆔 ID: <code>{view.telegram_id}</code>")

    return "\n".join(lines)


@router.message(Command(commands=[ME]))
async def cmd_me_handler(message: Message, interactor: FromDishka[ReadCurrentUserQueryHandler]) -> None:
    query: ReadCurrentUserQuery = ReadCurrentUserQuery()
    view: UserView = await interactor(query)
    await message.reply(
        text=format_view(view),
        parse_mode=ParseMode.HTML
    )
