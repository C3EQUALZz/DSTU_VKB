from dataclasses import dataclass
from enum import StrEnum

from chat_service.application.common.query_params.pagination import Pagination
from chat_service.application.common.query_params.sorting import SortingOrder


class UserQueryFilters(StrEnum):
    name = "name"
    id = "id"


@dataclass(frozen=True, slots=True, kw_only=True)
class UserListSorting:
    sorting_field: UserQueryFilters
    sorting_order: SortingOrder


@dataclass(frozen=True, slots=True)
class UserListParams:
    pagination: Pagination
    sorting: UserListSorting
