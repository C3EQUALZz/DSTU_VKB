from chat_service.domain.common.errors.base import DomainFieldError


class EmptyContentMessageError(DomainFieldError):
    ...


class RussianSwearWordsMessageError(DomainFieldError):
    ...
