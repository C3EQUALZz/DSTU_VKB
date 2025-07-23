from cryptography_methods.domain.common.errors.base import DomainFieldError, DomainError


class NegativeKeyForClassicCaesarError(DomainFieldError):
    ...


class UnknownAlphabetError(DomainFieldError):
    ...


class BadKeyForClassicCaesarError(DomainFieldError):
    ...


class NumbersAreNotRelativelyPrime(DomainFieldError):
    ...


class CantFindModularInverse(DomainError):
    ...
