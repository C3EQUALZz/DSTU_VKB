from cryptography_methods.domain.common.errors.base import DomainFieldError


class NegativeKeyForClassicCaesarError(DomainFieldError):
    ...


class UnknownAlphabetError(DomainFieldError):
    ...


class BadKeyForClassicCaesarError(DomainFieldError):
    ...
