from chat_service.application.errors.base import ApplicationError


class PaginationError(ApplicationError): ...


class SortingError(ApplicationError): ...
