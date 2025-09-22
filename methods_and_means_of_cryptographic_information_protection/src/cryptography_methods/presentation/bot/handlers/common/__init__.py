from typing import Final, Iterable

from aiogram import Router

from .help import router as help_router
from .start import router as start_router

router: Final[Router] = Router()

sub_routers: Final[Iterable[Router]] = (
    start_router,
    help_router,
)

for sub_router in sub_routers:
    router.include_router(sub_router)
