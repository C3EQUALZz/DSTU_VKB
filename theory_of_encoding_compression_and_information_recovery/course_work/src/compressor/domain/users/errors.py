from compressor.domain.common.errors.base import DomainError, DomainFieldError


class SmallPasswordLength(DomainFieldError):
    ...


class UsernameError(DomainFieldError):
    ...


class EmptyFieldError(DomainFieldError):
    ...


class RoleAssignmentNotPermittedError(DomainError):
    ...


class CantChangeUsernameError(DomainError):
    ...


class TelegramIDMustBePositiveError(DomainError):
    ...


class InvalidTelegramUsernameError(DomainError):
    ...


class AuthorizationError(DomainError):
    ...


class ActivationChangeNotPermittedError(DomainError):
    ...


class RoleChangeNotPermittedError(DomainError):
    ...
