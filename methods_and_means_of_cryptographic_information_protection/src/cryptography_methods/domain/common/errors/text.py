from cryptography_methods.domain.common.errors.base import DomainFieldError


class TextCantContainsDigitsError(DomainFieldError):
    ...


class StringContainsMultipleLanguagesError(DomainFieldError):
    ...
