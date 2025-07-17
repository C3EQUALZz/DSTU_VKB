from cryptography_methods.domain.common.errors.base import DomainFieldError, DomainError


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


class RoleAssignmentNotPermittedError(DomainError):
    ...


class RoleChangeNotPermittedError(DomainError):
    ...


class TelegramAccountHasBeenLinkedError(DomainError):
    ...


class CantUnLinkUnexistingAccountError(DomainError):
    ...


class CantBlockSuperUserError(DomainError):
    ...


class BotCantBeLinkedToUserError(DomainError):
    ...


class UserAlreadyBlockedError(DomainError):
    ...


class AccessError(DomainError):
    ...
