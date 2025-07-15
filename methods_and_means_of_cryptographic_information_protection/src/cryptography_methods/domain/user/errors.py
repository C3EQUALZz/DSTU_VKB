from cryptography_methods.domain.common.errors.base import DomainFieldError


class UserNameCantBeEmptyStringError(DomainFieldError):
    ...


class UserNameCantBeNumberError(DomainFieldError):
    ...


class UserNameLengthError(DomainFieldError):
    ...


class UserSecondNameCantBeEmptyString(DomainFieldError):
    ...


class UserSecondNameCantBeNumberError(DomainFieldError):
    ...


class UserSecondNameLengthError(DomainFieldError):
    ...


class UserMiddleNameCantBeEmptyString(DomainFieldError):
    ...


class UserMiddleNameCantBeNumberError(DomainFieldError):
    ...


class UserMiddleNameLengthError(DomainFieldError):
    ...
