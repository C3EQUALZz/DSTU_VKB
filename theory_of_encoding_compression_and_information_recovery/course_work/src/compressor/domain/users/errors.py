from compressor.domain.common.errors.base import DomainFieldError


class SmallPasswordLength(DomainFieldError):
    ...


class UsernameError(DomainFieldError):
    ...
