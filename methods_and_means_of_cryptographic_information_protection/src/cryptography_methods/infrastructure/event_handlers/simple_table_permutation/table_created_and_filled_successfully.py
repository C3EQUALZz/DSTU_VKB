from typing import Final, final

from bazario.asyncio import NotificationHandler
from typing_extensions import override

from cryptography_methods.application.common.id_provider import IdentityProvider
from cryptography_methods.application.common.view_manager import ViewManager
from cryptography_methods.domain.cipher_table.events import TableCreatedAndFilledSuccessfullyEvent
from cryptography_methods.domain.user.values.user_id import UserID


@final
class SendToUserTableCreatedAndFilledSuccessfullyEventHandler(NotificationHandler[TableCreatedAndFilledSuccessfullyEvent]):
    def __init__(self, view_manager: ViewManager, idp: IdentityProvider) -> None:
        self._view_manager: Final[ViewManager] = view_manager
        self._idp: Final[IdentityProvider] = idp

    @override
    async def handle(self, notification: TableCreatedAndFilledSuccessfullyEvent) -> None:
        user_id: UserID = await self._idp.get_current_user_id()

        await self._view_manager.send_table_to_user(
            user_id=user_id,
            table=notification.table,
        )
