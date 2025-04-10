from functools import lru_cache

from dishka import AsyncContainer, make_async_container


@lru_cache(maxsize=1)
def get_container() -> AsyncContainer:
    return make_async_container()
