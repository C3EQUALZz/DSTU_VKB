from typing_extensions import override

from compressor.application.common.ports.access_revoker import AccessRevoker
from compressor.domain.users.values.user_id import UserID


class TelegramAccessRevoker(AccessRevoker):
    """
    In telegram we doesn't have sessions or other mechanism to remove all user access.
    So here, we provide nothing.
    If backend uses application, then you must provide here logic with auth session.
    """

    @override
    async def remove_all_user_access(self, user_id: UserID) -> None:
        ...
