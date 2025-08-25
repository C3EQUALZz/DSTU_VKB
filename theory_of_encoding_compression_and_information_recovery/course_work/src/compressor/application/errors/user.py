from compressor.application.errors.base import ApplicationError


class UserNotFoundError(ApplicationError):
    ...


class UserAlreadyExistsError(ApplicationError):
    ...


class UserHasLinkedTelegramAccountBeforeError(ApplicationError):
    ...


class UserIsBotError(ApplicationError):
    ...
